import torch
import random
from collections import defaultdict

def get_enhanced_recommendations(model, pyg_graph, fashion_graph, item_id, node_mapping, fashion_data, top_k=5, verbose=True):
    """
    Get top-k fashion item recommendations for a given item,
    following gender and product group compatibility rules:
    
    - Lady and men items shouldn't be paired together, but both can pair with divided (neutral)
    - "Garment Full body" shouldn't be paired with "Garment Upper body" or "Garment Lower body"
    
    Args:
        model: Trained FashionGAT model
        pyg_graph: PyTorch Geometric graph
        fashion_graph: NetworkX graph
        item_id: ID of the item to get recommendations for
        node_mapping: Mapping between node names and indices
        fashion_data: Original fashion dataframe
        top_k: Number of recommendations to return
        verbose: Whether to print progress
        
    Returns:
        List of (item_id, score, explanation) tuples
    """
    if verbose:
        print(f"Finding recommendations for item ID {item_id}...")
    
    device = torch.device('cpu')
    model = model.to(device)
    
    # Get item node and index
    item_node = f"item_{item_id}"
    try:
        item_idx = node_mapping['item'][item_node]
    except KeyError:
        raise ValueError(f"Item ID {item_id} not found in the graph")
    
    # Get query item details
    try:
        item_row = fashion_data[fashion_data['article_id'] == item_id].iloc[0]
        item_name = item_row['prod_name']
        item_product_group = item_row['product_group_name']
        item_gender_group = item_row['index_group_no']
        item_gender_name = item_row['index_group_name']
    except Exception as e:
        print(f"Error getting item details: {str(e)}")
        print("Attempting to get details from graph...")
        try:
            item_name = fashion_graph.nodes[item_node].get('name', 'Unknown')
            item_product_group = fashion_graph.nodes[item_node].get('product_group', 'Unknown')
            item_gender_group = fashion_graph.nodes[item_node].get('gender_group', 0)
            item_gender_name = fashion_graph.nodes[item_node].get('gender_name', 'Unknown')
        except Exception as e:
            print(f"Error getting details from graph: {str(e)}")
            raise ValueError(f"Could not find details for item ID {item_id} in either dataset or graph")
    
    if verbose:
        print(f"Finding recommendations for: {item_name} (Group: {item_product_group}, Gender: {item_gender_name})")
    
    # Pre-filter items based on gender and product group compatibility
    filtered_indices = []
    filtered_ids = []
    
    # Track filtered items for statistics
    filtered_gender = 0
    filtered_product_group = 0
    filtered_same_group = 0
    
    incompatible_groups = [
        ("Garment Full body", "Garment Upper body"),
        ("Garment Full body", "Garment Lower body"),
        ("Garment Upper body", "Garment Full body"),
        ("Garment Lower body", "Garment Full body")
    ]
    
    # Create a mask for compatible items
    all_items = list(node_mapping['item'].keys())
    for other_node in all_items:
        if other_node == item_node:
            continue
            
        other_idx = node_mapping['item'][other_node]
        other_id = int(other_node.split('_')[1])
        
        try:
            other_row = fashion_data[fashion_data['article_id'] == other_id].iloc[0]
            other_product_group = other_row['product_group_name']
            other_gender_group = other_row['index_group_no']
        except:
            other_product_group = fashion_graph.nodes[other_node].get('product_group', 'Unknown')
            other_gender_group = fashion_graph.nodes[other_node].get('gender_group', 0)
        
        # Check gender compatibility
        if item_gender_group != other_gender_group:
            if (item_gender_group in [1, 2] and other_gender_group in [1, 2] and 
                item_gender_group != other_gender_group):
                filtered_gender += 1
                continue
        
        # Check product group compatibility
        if (item_product_group, other_product_group) in incompatible_groups:
            filtered_product_group += 1
            continue
        
        # Filter same product group
        if other_product_group == item_product_group:
            filtered_same_group += 1
            continue
            
        filtered_indices.append(other_idx)
        filtered_ids.append(other_id)
    
    if not filtered_indices:
        if verbose:
            print("No compatible items found after filtering.")
        return []
    
    # Convert to tensors
    filtered_indices = torch.tensor(filtered_indices, device=device)
    
    # Forward pass to get embeddings (only once)
    model.eval()
    with torch.no_grad():
        x_dict = {node_type: data.x.to(device) for node_type, data in pyg_graph.items()}
        edge_index_dict = {
            edge_type: data.edge_index.to(device) 
            for edge_type, data in pyg_graph.items() 
            if hasattr(data, 'edge_index')
        }
        node_embeddings = model(x_dict, edge_index_dict)
        item_embeddings = node_embeddings['item']
    
    # Compute compatibility scores in batches
    batch_size = 512
    all_scores = []
    
    for i in range(0, len(filtered_indices), batch_size):
        batch_indices = filtered_indices[i:i + batch_size]
        batch_scores = model.batch_predict_compatibility(
            torch.full((len(batch_indices),), item_idx, device=device),
            batch_indices,
            item_embeddings
        )
        all_scores.extend(list(zip(filtered_ids[i:i + batch_size], batch_scores.tolist())))
    
    # Sort by score and get top-k
    top_items = sorted(all_scores, key=lambda x: x[1], reverse=True)[:top_k]
    
    # Create final recommendations with explanations
    final_recommendations = []
    for item_id, score in top_items:
        # Compute attribute importance for top-k items
        attr_importance = model.compute_attribute_importance(
            item_idx, 
            node_mapping['item'][f"item_{item_id}"], 
            item_embeddings
        )
        
        # Get explanation
        explanation = explain_enhanced_compatibility(
            fashion_graph, item_node, f"item_{item_id}", 
            score, attr_importance, fashion_data
        )
        
        final_recommendations.append((item_id, score, explanation))
    
    if verbose:
        print(f"Found {len(final_recommendations)} recommendations.")
        print(f"Filtered {filtered_gender} items due to gender incompatibility.")
        print(f"Filtered {filtered_product_group} items due to product group incompatibility.")
        print(f"Filtered {filtered_same_group} items from the same product group.")
    
    return final_recommendations

def explain_enhanced_compatibility(fashion_graph, item1_node, item2_node, score, attr_importance, fashion_data):
    """
    Generate a natural and meaningful explanation for why two items are compatible.
    Now uses normalized attribute importance scores that represent percentages of influence.
    """
    # Get item details
    item1_id = int(item1_node.split('_')[1])
    item2_id = int(item2_node.split('_')[1])
    
    try:
        item1_row = fashion_data[fashion_data['article_id'] == item1_id].iloc[0]
        item1_name = item1_row['prod_name']
        item1_product_group = item1_row['product_group_name']
    except:
        item1_name = fashion_graph.nodes[item1_node].get('name', 'Unknown')
        item1_product_group = fashion_graph.nodes[item1_node].get('product_group', 'Unknown')
    
    try:
        item2_row = fashion_data[fashion_data['article_id'] == item2_id].iloc[0]
        item2_name = item2_row['prod_name']
        item2_product_group = item2_row['product_group_name']
    except:
        item2_name = fashion_graph.nodes[item2_node].get('name', 'Unknown')
        item2_product_group = fashion_graph.nodes[item2_node].get('product_group', 'Unknown')
    
    # Get attributes
    item1_attrs = get_item_attributes(fashion_graph, item1_node)
    item2_attrs = get_item_attributes(fashion_graph, item2_node)
    
    # Create base explanation structure
    explanation = {
        'score': score,
        'item1': {
            'id': item1_id,
            'name': item1_name,
            'product_group': item1_product_group,
            'attributes': item1_attrs
        },
        'item2': {
            'id': item2_id,
            'name': item2_name,
            'product_group': item2_product_group,
            'attributes': item2_attrs
        },
        'reasons': [],
        'attribute_importance': attr_importance
    }
    
    reasons = []
    
    # Style Combination - now weighted by appearance importance
    style_reason = f"This {item2_product_group.lower()} pairs well with the {item1_product_group.lower()}"
    if item1_attrs.get('appearance') and item2_attrs.get('appearance'):
        style_reason += f", creating a {item2_attrs['appearance'].lower()} look with {item1_attrs['appearance'].lower()} elements"
    style_reason += "."
    reasons.append({
        'type': 'style_combination',
        'description': style_reason,
        'importance': attr_importance.get('appearance', 0.0)
    })
    
    # Color Harmony - now weighted by color importance
    if 'color_master' in item1_attrs and 'color_master' in item2_attrs:
        color1 = item1_attrs['color_master'].replace('master_', '')
        color2 = item2_attrs['color_master'].replace('master_', '')
        
        if color1 == color2:
            reasons.append({
                'type': 'color_harmony',
                'description': f"The matching {color1.lower()} tones create a cohesive look.",
                'importance': attr_importance.get('color_master', 0.0)
            })
        else:
            reasons.append({
                'type': 'color_harmony',
                'description': f"The {color1.lower()} complements the {color2.lower()} beautifully.",
                'importance': attr_importance.get('color_master', 0.0)
            })
    
    # Luminance Balance - now weighted by luminance importance
    if 'color_value' in item1_attrs and 'color_value' in item2_attrs:
        luminance1 = item1_attrs['color_value'].replace('value_', '')
        luminance2 = item2_attrs['color_value'].replace('value_', '')
        
        if luminance1 == luminance2:
            reasons.append({
                'type': 'luminance_balance',
                'description': f"The consistent {luminance1.lower()} luminance creates a harmonious look.",
                'importance': attr_importance.get('color_value', 0.0)
            })
        else:
            reasons.append({
                'type': 'luminance_balance',
                'description': f"The {luminance1.lower()} and {luminance2.lower()} luminance levels create an interesting contrast.",
                'importance': attr_importance.get('color_value', 0.0)
            })
    
    # Texture Balance - now weighted by fabric importance
    if 'fabric' in item1_attrs and 'fabric' in item2_attrs:
        fabrics1 = item1_attrs['fabric'] if isinstance(item1_attrs['fabric'], list) else [item1_attrs['fabric']]
        fabrics2 = item2_attrs['fabric'] if isinstance(item2_attrs['fabric'], list) else [item2_attrs['fabric']]
        
        fabric_desc = f"The combination of {', '.join(fabrics1).lower()} with {', '.join(fabrics2).lower()} "
        if any(f in ['silk', 'satin', 'velvet', 'leather'] for f in fabrics1 + fabrics2):
            fabric_desc += "adds luxurious texture contrast."
        else:
            fabric_desc += "creates an interesting texture mix."
        
        reasons.append({
            'type': 'texture_balance',
            'description': fabric_desc,
            'importance': attr_importance.get('fabric', 0.0)
        })
    
    # Proportion Balance - now weighted by length importance
    if 'length' in item1_attrs and 'length' in item2_attrs:
        length1 = item1_attrs['length'].replace('_', ' ')
        length2 = item2_attrs['length'].replace('_', ' ')
        
        if ('crop' in length1 and 'high_waisted' in length2) or ('crop' in length2 and 'high_waisted' in length1):
            reasons.append({
                'type': 'proportion_balance',
                'description': "The cropped length pairs perfectly with the high-waisted style, creating a balanced silhouette.",
                'importance': attr_importance.get('length', 0.0)
            })
        elif ('long' in length1 and 'short' in length2) or ('long' in length2 and 'short' in length1):
            reasons.append({
                'type': 'proportion_balance',
                'description': "The contrast between the lengths creates an interesting and balanced proportion.",
                'importance': attr_importance.get('length', 0.0)
            })
        else:
            reasons.append({
                'type': 'proportion_balance',
                'description': f"The {length1.lower()} length works harmoniously with the {length2.lower()} length.",
                'importance': attr_importance.get('length', 0.0)
            })
    
    # Seasonal Coordination - now weighted by sleeve importance
    if 'sleeve' in item1_attrs and 'sleeve' in item2_attrs:
        sleeve1 = item1_attrs['sleeve'].replace('_', ' ')
        sleeve2 = item2_attrs['sleeve'].replace('_', ' ')
        
        if any(s in (sleeve1 + sleeve2).lower() for s in ['sleeveless', 'short']):
            reasons.append({
                'type': 'seasonal_coordination',
                'description': "Perfect for warmer weather with its lightweight sleeve combination.",
                'importance': attr_importance.get('sleeve', 0.0)
            })
        elif any(s in (sleeve1 + sleeve2).lower() for s in ['long', 'full']):
            reasons.append({
                'type': 'seasonal_coordination',
                'description': "Ideal for cooler weather with its cozy sleeve styling.",
                'importance': attr_importance.get('sleeve', 0.0)
            })
    
    # Neckline Harmony - now weighted by neckline importance
    if 'neckline' in item1_attrs and 'neckline' in item2_attrs:
        neck1 = item1_attrs['neckline'].replace('_', ' ')
        neck2 = item2_attrs['neckline'].replace('_', ' ')
        
        if 'high' in (neck1 + neck2).lower():
            reasons.append({
                'type': 'neckline_harmony',
                'description': "The high neckline adds sophistication to the overall look.",
                'importance': attr_importance.get('neckline', 0.0)
            })
        elif 'v' in (neck1 + neck2).lower():
            reasons.append({
                'type': 'neckline_harmony',
                'description': "The v-neckline creates an elongating effect that enhances the silhouette.",
                'importance': attr_importance.get('neckline', 0.0)
            })
        else:
            reasons.append({
                'type': 'neckline_harmony',
                'description': f"The {neck1.lower()} neckline style complements the overall look.",
                'importance': attr_importance.get('neckline', 0.0)
            })
    
    # Sort reasons by importance score and take top 3
    sorted_reasons = sorted(reasons, key=lambda x: x['importance'], reverse=True)
    explanation['reasons'] = [reason for reason in sorted_reasons[:3]]
    
    return explanation

def get_item_attributes(graph, item_node):
    """Extract all attributes of an item from the graph"""
    attrs = {}
    
    # Helper function to find attribute values
    def find_attribute_value(attr_prefix):
        for neighbor in graph.neighbors(item_node):
            if neighbor.startswith(f"attr_{attr_prefix}"):
                # Found attribute node, now find its value
                for val_node in graph.neighbors(neighbor):
                    if val_node != item_node and val_node.startswith(f"val_{attr_prefix}"):
                        # Extract the value name
                        val_parts = val_node.split('_')
                        if len(val_parts) > 2:
                            return '_'.join(val_parts[2:])  # Skip "val_attr_" prefix
                        else:
                            return val_parts[-1]
        return None
    
    # Find fabric values (can be multiple)
    def find_fabric_values():
        fabrics = []
        for neighbor in graph.neighbors(item_node):
            if neighbor.startswith("attr_fabric_"):
                for val_node in graph.neighbors(neighbor):
                    if val_node != item_node and val_node.startswith("val_fabric_"):
                        # Extract the fabric name
                        val_parts = val_node.split('_')
                        if len(val_parts) > 2:  # Has prefix
                            fabric = '_'.join(val_parts[2:])
                        else:
                            fabric = val_parts[-1]
                        
                        if fabric and fabric not in fabrics:
                            fabrics.append(fabric)
        return fabrics if fabrics else None
    
    # Get all attribute values
    attrs['product_type'] = find_attribute_value('product_type')
    attrs['color_value'] = find_attribute_value('color_value')
    attrs['color_master'] = find_attribute_value('color_master')
    attrs['appearance'] = find_attribute_value('appearance')
    attrs['fabric'] = find_fabric_values()
    attrs['sleeve'] = find_attribute_value('sleeve')
    attrs['length'] = find_attribute_value('length')
    attrs['neckline'] = find_attribute_value('neckline')
    
    # Remove None values
    attrs = {k: v for k, v in attrs.items() if v}
    
    return attrs

def format_enhanced_recommendations(recommendations, fashion_data):
    """Format recommendation results for display"""
    results = []
    
    for rec_id, score, explanation in recommendations:
        # Get item details from the dataset
        try:
            item_data = fashion_data[fashion_data['article_id'] == rec_id].iloc[0]
            name = item_data['prod_name']
            product_group = item_data['product_group_name']
        except:
            # Use data from explanation if item not found in dataset
            name = explanation['item2']['name']
            product_group = explanation['item2']['product_group']
        
        result = {
            'item_id': rec_id,
            'name': name,
            'product_group': product_group,
            'compatibility_score': score,
            'explanation': explanation['reasons'],
            'attribute_importance': explanation['attribute_importance'],
            'attributes': explanation['item2']['attributes']
        }
        
        results.append(result)
    
    return results

def display_recommendations(item_id, recommendations, fashion_data):
    """Display formatted recommendations for a query item"""
    # Get query item details
    query_item = fashion_data[fashion_data['article_id'] == item_id].iloc[0]
    print(f"\nQuery Item:")
    print(f"ID: {item_id}")
    print(f"Name: {query_item['prod_name']}")
    print(f"Product Group: {query_item['product_group_name']}")
    print("\nKey Attributes:")
    print(f"  - Color: {query_item['perceived_colour_value_name']}")
    print(f"  - Luminance: {query_item['perceived_colour_master_name']}")
    print(f"  - Appearance: {query_item['graphical_appearance_name']}")
    if query_item['parsed_fabrics']:
        print(f"  - Fabric: {', '.join(query_item['parsed_fabrics'])}")
    if query_item['Sleeve_prediction']:
        print(f"  - Sleeve: {query_item['Sleeve_prediction']}")
    if query_item['Length_prediction']:
        print(f"  - Length: {query_item['Length_prediction']}")
    if query_item['Neckline_prediction']:
        print(f"  - Neckline: {query_item['Neckline_prediction']}")
    
    print("\nRecommended Items:")
    for i, rec in enumerate(recommendations, 1):
        # Handle both tuple and dictionary formats
        if isinstance(rec, tuple):
            rec_id, score, explanation = rec
            # Get item details from the dataset
            try:
                item_data = fashion_data[fashion_data['article_id'] == rec_id].iloc[0]
                name = item_data['prod_name']
                product_group = item_data['product_group_name']
            except:
                name = "Unknown"
                product_group = "Unknown"
            
            print(f"\n{i}. ID: {rec_id}")
            print(f"   Name: {name}")
            print(f"   Product Group: {product_group}")
            print(f"   Compatibility Score: {score:.3f}")
            
            # Display explanation reasons
            if explanation and 'reasons' in explanation:
                print("   Why This Match Works:")
                for reason in explanation['reasons']:
                    # Replace internal attribute names with user-friendly names in the explanation
                    reason_text = reason['description']
                    reason_text = reason_text.replace('color_master', 'Color')
                    reason_text = reason_text.replace('color_value', 'Luminance')
                    reason_text = reason_text.replace('value_', '')
                    reason_text = reason_text.replace('master_', '')
                    print(f"     - {reason_text}")
            
            # Display attribute importance scores
            if explanation and 'attribute_importance' in explanation:
                print("\n   Attribute Importance:")
                attr_importance = explanation['attribute_importance']
                # Sort attributes by importance score
                sorted_attrs = sorted(attr_importance.items(), key=lambda x: x[1], reverse=True)
                for attr, importance in sorted_attrs:
                    display_attr = {
                        'color_master': 'Color',
                        'color_value': 'Luminance',
                        'appearance': 'Appearance',
                        'fabric': 'Fabric',
                        'sleeve': 'Sleeve',
                        'length': 'Length',
                        'neckline': 'Neckline'
                    }.get(attr, attr.capitalize())
                    print(f"     - {display_attr}: {importance:.3f}")
            
            # Display attributes if available
            if explanation and 'item2' in explanation and 'attributes' in explanation['item2']:
                print("\n   Key Attributes:")
                for attr, value in explanation['item2']['attributes'].items():
                    if attr in ['color_value', 'color_master', 'appearance', 'fabric', 'sleeve', 'length', 'neckline']:
                        if isinstance(value, list):
                            value_str = ', '.join(value)
                        else:
                            value_str = value
                        # Map attribute names to display labels and clean up values
                        display_attr = {
                            'color_master': 'Color',
                            'color_value': 'Luminance',
                            'appearance': 'Appearance',
                            'fabric': 'Fabric',
                            'sleeve': 'Sleeve',
                            'length': 'Length',
                            'neckline': 'Neckline'
                        }.get(attr, attr.capitalize())
                        
                        # Remove value_ and master_ prefixes from color and luminance values
                        if attr == 'color_value' and value_str.startswith('value_'):
                            value_str = value_str[6:]  # Remove 'value_' prefix
                        elif attr == 'color_master' and value_str.startswith('master_'):
                            value_str = value_str[7:]  # Remove 'master_' prefix
                        
                        print(f"     - {display_attr}: {value_str}")
        else:
            # Handle dictionary format
            print(f"\n{i}. ID: {rec['item_id']}")
            print(f"   Name: {rec['name']}")
            print(f"   Product Group: {rec['product_group']}")
            print(f"   Compatibility Score: {rec['compatibility_score']:.3f}")
            
            # Display explanation reasons
            if 'explanation' in rec:
                print("   Why This Match Works:")
                for reason in rec['explanation']:
                    # Replace internal attribute names with user-friendly names in the explanation
                    reason_text = reason['description']
                    reason_text = reason_text.replace('color_master', 'Color')
                    reason_text = reason_text.replace('color_value', 'Luminance')
                    reason_text = reason_text.replace('value_', '')
                    reason_text = reason_text.replace('master_', '')
                    print(f"     - {reason_text}")
            
            # Display attribute importance scores
            if 'attribute_importance' in rec:
                print("\n   Attribute Importance:")
                attr_importance = rec['attribute_importance']
                # Sort attributes by importance score
                sorted_attrs = sorted(attr_importance.items(), key=lambda x: x[1], reverse=True)
                for attr, importance in sorted_attrs:
                    display_attr = {
                        'color_master': 'Color',
                        'color_value': 'Luminance',
                        'appearance': 'Appearance',
                        'fabric': 'Fabric',
                        'sleeve': 'Sleeve',
                        'length': 'Length',
                        'neckline': 'Neckline'
                    }.get(attr, attr.capitalize())
                    print(f"     - {display_attr}: {importance:.3f}")
            
            # Display attributes
            if 'attributes' in rec:
                print("\n   Key Attributes:")
                for attr, value in rec['attributes'].items():
                    if attr in ['color_value', 'color_master', 'appearance', 'fabric', 'sleeve', 'length', 'neckline']:
                        if isinstance(value, list):
                            value_str = ', '.join(value)
                        else:
                            value_str = value
                        # Map attribute names to display labels and clean up values
                        display_attr = {
                            'color_master': 'Color',
                            'color_value': 'Luminance',
                            'appearance': 'Appearance',
                            'fabric': 'Fabric',
                            'sleeve': 'Sleeve',
                            'length': 'Length',
                            'neckline': 'Neckline'
                        }.get(attr, attr.capitalize())
                        
                        # Remove value_ and master_ prefixes from color and luminance values
                        if attr == 'color_value' and value_str.startswith('value_'):
                            value_str = value_str[6:]  # Remove 'value_' prefix
                        elif attr == 'color_master' and value_str.startswith('master_'):
                            value_str = value_str[7:]  # Remove 'master_' prefix
                        
                        print(f"     - {display_attr}: {value_str}")
        
        print()

def save_model_and_data(model, fashion_graph, pyg_graph, node_mapping, fashion_data, output_dir="fashion_model"):
    """Save model and graph data for later use"""
    import os
    import pickle
    import torch
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save model
    torch.save(model.state_dict(), os.path.join(output_dir, "gat_model.pt"))
    
    # Save graph data using pickle
    with open(os.path.join(output_dir, "fashion_graph.pkl"), "wb") as f:
        pickle.dump(fashion_graph, f)
    
    with open(os.path.join(output_dir, "node_mapping.pkl"), "wb") as f:
        pickle.dump(node_mapping, f)
    
    # Save PyG graph tensors
    torch.save(pyg_graph, os.path.join(output_dir, "pyg_graph.pt"))
    
    # Save the full dataset for lookups
    fashion_data.to_csv(os.path.join(output_dir, "full_data.csv"), index=False)
    
    print(f"Model and data saved to {output_dir}/")

def load_model_and_data(model_class, output_dir="fashion_model", **model_kwargs):
    """Load saved model and graph data"""
    import os
    import pickle
    import torch
    import pandas as pd
    from torch_geometric.data.storage import BaseStorage, NodeStorage, EdgeStorage
    
    # Add required classes to safe globals for PyTorch 2.6 compatibility
    torch.serialization.add_safe_globals([BaseStorage, NodeStorage, EdgeStorage])
    
    # Load model
    model_path = os.path.join(output_dir, "gat_model.pt")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    
    # Load PyG graph with weights_only=False for PyTorch 2.6 compatibility
    pyg_graph = torch.load(os.path.join(output_dir, "pyg_graph.pt"), weights_only=False)
    
    # Create model with provided parameters
    model = model_class(pyg_graph, **model_kwargs)
    model.load_state_dict(torch.load(model_path, weights_only=False))
    model.eval()
    
    # Load graph data
    with open(os.path.join(output_dir, "fashion_graph.pkl"), "rb") as f:
        fashion_graph = pickle.load(f)
    
    with open(os.path.join(output_dir, "node_mapping.pkl"), "rb") as f:
        node_mapping = pickle.load(f)
    
    # Load fashion data sample
    fashion_data = pd.read_csv(os.path.join(output_dir, "full_data.csv"))
    
    # Debug prints
    print(f"\nDebug: Checking data loading...")
    print(f"Number of items in fashion_data: {len(fashion_data)}")
    print(f"Number of unique article IDs: {fashion_data['article_id'].nunique()}")
    # Sample 5 random article IDs instead of just the first 5
    random_sample = fashion_data['article_id'].sample(5).tolist()
    print(f"Sample of random article IDs: {random_sample}")
    
    # Check if specific item exists
    test_id = 860260001
    print(f"\nChecking for item {test_id}:")
    print(f"Exists in dataset: {test_id in fashion_data['article_id'].values}")
    print(f"Exists in graph: {f'item_{test_id}' in fashion_graph.nodes}")
    print(f"Exists in node mapping: {f'item_{test_id}' in node_mapping['item']}")
    
    print(f"Model and data loaded from {output_dir}/")
    
    return model, fashion_graph, pyg_graph, node_mapping, fashion_data