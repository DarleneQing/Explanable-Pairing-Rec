import pandas as pd
import torch
from torch_geometric.data.storage import BaseStorage, NodeStorage, EdgeStorage
from .models import Item, RecItem, Session
from datetime import datetime
import uuid
import os
from typing import Dict, Optional, List
import threading
import time

# Now that data is inside backend, we can use relative imports
try:
    from .data.Enhancement import load_model_and_data, get_enhanced_recommendations, display_recommendations
    from .data.Recommender import EnhancedFashionGAT
    data_modules_available = True
    print("✅ Data modules imported successfully")
except ImportError as e:
    print(f"⚠️  Warning: Could not import data modules: {e}")
    print("   Recommendation functionality will be disabled")
    data_modules_available = False

torch.serialization.add_safe_globals([BaseStorage, NodeStorage, EdgeStorage])

# Global variables for model (will be loaded asynchronously)
model = None
fashion_graph = None
pyg_graph = None 
node_mapping = None
fashion_data = None
model_loading = False
model_loaded = False

def load_model_async():
    """Load model asynchronously to avoid blocking server startup"""
    global model, fashion_graph, pyg_graph, node_mapping, fashion_data, model_loading, model_loaded
    
    if not data_modules_available:
        print("⚠️  Data modules not available, skipping model loading")
        return
    
    model_loading = True
    print("🤖 Starting async model loading...")
    
    try:
        # Try to find model directory
        model_paths = [
            "./backend/data/model_data",  # When running from project root
            "./data/model_data",          # When running from backend directory
            "data/model_data"             # Alternative path
        ]
        
        model_path = None
        for path in model_paths:
            if os.path.exists(path):
                model_path = path
                break
        
        if model_path is None:
            print("⚠️  Model directory not found, skipping model loading")
            model_loading = False
            return
            
        print(f"📂 Loading model from: {model_path}")
        
        # Add timeout to prevent hanging
        start_time = time.time()
        model, fashion_graph, pyg_graph, node_mapping, fashion_data = load_model_and_data(
            EnhancedFashionGAT, model_path,
            hidden_channels=128,
            out_channels=64
        )
        
        load_time = time.time() - start_time
        print(f"✅ Model loaded successfully in {load_time:.2f} seconds!")
        model_loaded = True
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        model = None
        fashion_graph = None
        pyg_graph = None 
        node_mapping = None
        fashion_data = None
        model_loaded = False
    finally:
        model_loading = False

# Start model loading in background thread (non-blocking)
if data_modules_available:
    print("🚀 Starting background model loading...")
    model_thread = threading.Thread(target=load_model_async, daemon=True)
    model_thread.start()
else:
    print("⚠️  Skipping model loading - data modules not available")

class Repository:
    def __init__(self):
        print("🏗️  Initializing Repository...")
        
        # Quick CSV loading with timeout protection
        try:
            csv_path = self._find_csv_file()
            if csv_path is None:
                raise FileNotFoundError("item_metadata.csv not found in any expected location")
            
            print(f"📊 Loading CSV from: {csv_path}")
            start_time = time.time()
            
            # Load with chunksize to prevent memory issues
            self._df = pd.read_csv(csv_path)
            
            load_time = time.time() - start_time
            print(f"📈 Loaded {len(self._df)} items from CSV in {load_time:.2f} seconds")
            
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            # Create empty dataframe as fallback
            self._df = pd.DataFrame()
        
        # Initialize session storage
        self._sessions: Dict[str, Session] = {}
        self._session_query_items: Dict[str, Item] = {}
        self._session_recommendations: Dict[str, List[RecItem]] = {}
        self._session_rec_generated: Dict[str, bool] = {}
        
        print("✅ Repository initialized successfully")
    
    def _find_csv_file(self) -> Optional[str]:
        """Find CSV file with timeout protection"""
        csv_paths = [
            "./backend/data/item_metadata.csv",  # When running from project root
            "./data/item_metadata.csv",          # When running from backend directory  
            "backend/data/item_metadata.csv",    # Alternative from project root
            "data/item_metadata.csv"             # Alternative from backend
        ]
        
        for path in csv_paths:
            try:
                if os.path.exists(path):
                    return path
            except Exception as e:
                print(f"⚠️  Error checking path {path}: {e}")
                continue
        
        print(f"❌ CSV file not found. Current dir: {os.getcwd()}")
        print("Checked paths:")
        for path in csv_paths:
            print(f"  - {path}: {os.path.exists(path) if path else 'Invalid path'}")
        
        return None

    def create_session(self) -> Session:
        session = Session(
            session_id=str(uuid.uuid4()),
            created_at=datetime.now(),
            is_active=True,
        )
        # Store session by its ID
        self._sessions[session.session_id] = session
        # Initialize recommendation tracking
        self._session_rec_generated[session.session_id] = False
        
        print(f"📱 Session {session.session_id} created (model ready: {model is not None})")
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID"""
        return self._sessions.get(session_id)
    
    def update_session(self, session: Session) -> None:
        """Update an existing session"""
        self._sessions[session.session_id] = session
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session by ID"""
        if session_id in self._sessions:
            del self._sessions[session_id]
            # Also clean up related data
            self._session_query_items.pop(session_id, None)
            self._session_recommendations.pop(session_id, None)
            self._session_rec_generated.pop(session_id, None)
            print(f"🗑️  Session {session_id} deleted and cleaned up")
            return True
        return False
    
    def get_active_sessions(self) -> list[Session]:
        """Get all active sessions"""
        return [session for session in self._sessions.values() if session.is_active]
    
    def put_query_item(self, session_id: str, article_id: int) -> bool:
        """Add query item to a specific session and prepare recommendations"""
        session = self.get_session(session_id)
        if session:
            item = self.get_metadata(article_id)
            if item:
                self._session_query_items[session_id] = item
                
                # Generate recommendations immediately when query item is set
                # This ensures the user won't have to wait later
                self._generate_recommendations_for_session(session_id, article_id)
                
                print(f"🎯 Query item set for session {session_id}: {article_id}")
                return True
        return False
    
    def _generate_recommendations_for_session(self, session_id: str, article_id: int) -> None:
        """Generate recommendations for a session based on the query item"""
        global model_loaded, model_loading
        
        # Check if model is available
        if not data_modules_available:
            print(f"⚠️  Cannot generate recommendations: data modules unavailable")
            self._session_recommendations[session_id] = []
            self._session_rec_generated[session_id] = False
            return
            
        if model_loading:
            print(f"⏳ Model still loading, recommendations will be empty for now")
            self._session_recommendations[session_id] = []
            self._session_rec_generated[session_id] = False
            return
            
        if not model_loaded or model is None or node_mapping is None:
            print(f"⚠️  Cannot generate recommendations: model not loaded")
            self._session_recommendations[session_id] = []
            self._session_rec_generated[session_id] = False
            return
            
        try:
            print(f"🔄 Generating recommendations for session {session_id}...")
            
            # Get enhanced recommendations using your model
            recommendations = get_enhanced_recommendations(
                model=model,
                fashion_graph=fashion_graph,
                pyg_graph=pyg_graph,
                node_mapping=node_mapping,
                fashion_data=fashion_data,
                item_id=article_id,
                top_k=50  # Generate top 50 recommendations
            )
            
            # Convert to RecItem objects
            rec_items = []
            for i in range(min(50, len(recommendations))):  # Use min to avoid index errors
                item_id = recommendations[i][2]['item2']['id']  # First element is the item_id (integer)
                compatibility_score = recommendations[i][2]['score']  # Second element is the score (float)
                attribute_importance = recommendations[i][2]['attribute_importance']
                
                rec_metadata = self.get_metadata(item_id)
                if rec_metadata:
                    rec_item = RecItem(
                        **rec_metadata.dict(),
                        compatibility_score=compatibility_score,
                        color_importance=attribute_importance.get('color_master', 0.0),
                        luminance_importance=attribute_importance.get('color_value', 0.0),
                        appearance_importance=attribute_importance.get('appearance', 0.0),
                        fabric_importance=attribute_importance.get('fabric', 0.0),
                        neckline_importance=attribute_importance.get('neckline', 0.0),
                        sleeve_importance=attribute_importance.get('sleeve', 0.0),
                        length_importance=attribute_importance.get('length', 0.0)
                    )
                    rec_items.append(rec_item)
            
            # Store recommendations for the session
            self._session_recommendations[session_id] = rec_items
            self._session_rec_generated[session_id] = True
            
            print(f"✅ Generated {len(rec_items)} recommendations for session {session_id}")
            
        except Exception as e:
            print(f"❌ Error generating recommendations for session {session_id}: {e}")
            # Store empty list as fallback
            self._session_recommendations[session_id] = []
            self._session_rec_generated[session_id] = False
    
    def get_query_item(self, session_id: str) -> Optional[Item]:
        """Get the query item for a session"""
        return self._session_query_items.get(session_id)
    
    def _handle_nan_value(self, value, default=""):
        """Convert NaN values to appropriate defaults"""
        import pandas as pd
        if pd.isna(value):
            return default
        return value
    
    def get_metadata(self, article_id: int) -> Optional[Item]:
        try:
            # Quick check if dataframe is empty
            if self._df.empty:
                print(f"⚠️  CSV data not loaded, cannot find article {article_id}")
                return None
                
            item = self._df[self._df["article_id"] == article_id]
            
            # Check if item exists
            if item.empty:
                # Only print this occasionally to avoid spam
                if article_id % 1000 == 0:  # Only for round numbers
                    print(f"❌ Article {article_id} not found in CSV")
                return None
            
            return Item(
                article_id=item["article_id"].values[0],
                prod_name=self._handle_nan_value(item["prod_name"].values[0]),
                prod_type_name=self._handle_nan_value(item["product_type_name"].values[0]),
                prod_group_name=self._handle_nan_value(item["product_group_name"].values[0]),
                graphical_appearance_name=self._handle_nan_value(item["graphical_appearance_name"].values[0]),
                colour_group_name=self._handle_nan_value(item["colour_group_name"].values[0]),
                perceived_colour_value_name=self._handle_nan_value(item["perceived_colour_value_name"].values[0]),
                perceived_colour_master_name=self._handle_nan_value(item["perceived_colour_master_name"].values[0]),
                index_group_name=self._handle_nan_value(item["index_group_name"].values[0]),
                garment_group_name=self._handle_nan_value(item["garment_group_name"].values[0]),
                detail_desc=self._handle_nan_value(item["detail_desc"].values[0]),
                sleeve_prediction=self._handle_nan_value(item["Sleeve_prediction"].values[0]),
                length_prediction=self._handle_nan_value(item["Length_prediction"].values[0]),
                neckline_prediction=self._handle_nan_value(item["Neckline_prediction"].values[0]),
                detected_fabrics=self._handle_nan_value(item["detected_fabrics"].values[0])
            )
        except Exception as e:
            print(f"❌ Error in get_metadata for article {article_id}: {e}")
            return None

    def get_recommendations(self, session_id: str) -> List[RecItem]:
        """Get recommendations for a specific session"""
        # Check if session exists
        if session_id not in self._sessions:
            return []
        
        # Check if recommendations have been generated
        if not self._session_rec_generated.get(session_id, False):
            print(f"ℹ️  No recommendations generated yet for session {session_id}")
            return []
        
        recommendations = self._session_recommendations.get(session_id, [])
        print(f"📋 Returning {len(recommendations)} recommendations for session {session_id}")
        return recommendations
    