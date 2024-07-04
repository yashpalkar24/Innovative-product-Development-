import streamlit as st
import requests
import json
import plotly.graph_objects as go
import random

st.title("SAFE SURF")
st.subheader("Privacy Policy Checker")

# Input field for URL
url = st.text_input("Enter URL:")

import plotly.graph_objects as go



#  # Assuming this is within your create_gauge function
# def create_gauge(score, max_score, total_risk):
#     fig = go.Figure(go.Indicator(
#         mode="gauge+number",
#         value=score,  # This should be directly the 'score' you want to display
#         domain={'x': [0, 1], 'y': [0, 1]},
#         gauge={
#             'axis': {
#                 'range': [None, max_score],  # Ensure max_score is the upper limit of your gauge
#                 'tickwidth': 1,
#                 'tickcolor': "darkblue",
#                 # Setting dynamic tickvals and ticktext if needed based on your scoring system
#                 'tickvals': [0, max_score * 0.25, max_score * 0.5, max_score * 0.75, max_score],
#                 'ticktext': ['Very Safe', 'Safe', 'Risk', 'Very Risky', 'Danger']
#             },
#             'bar': {'color': "darkblue"},  # Bar color can be adjusted if needed
#             'bgcolor': "white",
#             'borderwidth': 2,
#             'bordercolor': "gray",
#             'steps': [  # Color steps can also be dynamically set if needed
#                 {'range': [0, max_score * 0.25], 'color': 'lightgreen'},
#                 {'range': [max_score * 0.25, max_score * 0.5], 'color': 'yellow'},
#                 {'range': [max_score * 0.5, max_score * 0.75], 'color': 'orange'},
#                 {'range': [max_score * 0.75, max_score], 'color': 'red'}
#             ],
#             'threshold': {
#                 'line': {'color': "red", 'width': 4},
#                 'thickness': 0.75,
#                 'value': total_risk
            
                
            
#             }
#         }
#     ))

#     return fig   

import plotly.graph_objects as go

def create_gauge(score, max_score, total_risk):
    # Calculate percentage of the score relative to max_score
    percentage = (score / max_score) * 100

    # Create the gauge figure with Plotly
    fig = go.Figure(go.Indicator(
        mode="gauge+number",  # Displays the gauge and the number
        value=percentage,  # Use the percentage for the gauge value
        title={'text': f"{percentage:.1f}% (Score: {score}/{max_score})"},  # Additional details in the title
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100]},  # Axis now spans from 0 to 100%
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 25], 'color': 'lightgreen'},
                {'range': [25, 50], 'color': 'yellow'},
                {'range': [50, 75], 'color': 'orange'},
                {'range': [75, 100], 'color': 'red'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': (total_risk / max_score) * 100  # Assuming total_risk is also to be shown as a percentage
            }
        }
    ))

    return fig





def simulate_api_call():
    """ Simulate API response """
    return {
        'status': 'DONE',
        'data': {
            'score': random.randint(10, 100),
            'maxScore': 100,
            'totalRisk': random.randint(10, 100)
        }
    }

def calculate_score(value, ranges):
    """Calculate the score rating for a given value based on specified ranges."""
    for i, range_max in enumerate(ranges):
        if value <= range_max:
            return f"{i}/5"
    return f"{len(ranges)}/5"

def fetch_data(url):
    """ Fetch data from the server and handle errors. """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        st.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        st.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        st.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        st.error(f"Other Error: {err}")
        return None  # Return None to indicate failure
    
def generate_random_values():
    score = random.randint(60, 80)
    max_score = random.randint(60, 80)
    total_risk = random.randint(60, 80)
    return score, max_score, total_risk


ranges = [50, 100, 150, 200, 250]  # Define the maximum values for each rating level

# Button to trigger genReport API call  
if st.button("Generate Report"):
    if url and id:
        try:
            response = requests.get(f"http://127.0.0.1:5000/genReport?id={id}&url={url}")
            response.raise_for_status()  # Checks if the request was successful
            result = response.json()

            # Extract score and risk from JSON response
            score = result.get('data', {}).get('score', 0)
            max_score = result.get('data', {}).get('maxScore', 100)
            total_risk = result.get('data', {}).get('totalRisk', 0)
            

      
            result = fetch_data(url)  # Assume this function returns the fetched data as a dictionary
            if result and result['status'] == 'DONE':
                max_score = result['data']['maxScore']
                total_risk = result['data']['totalRisk']
            
            score_rating = calculate_score(max_score, ranges)
            risk_rating = calculate_score(total_risk, ranges)

            # Create and display gauge
            gauge_fig = create_gauge(score, max_score, total_risk)
            st.plotly_chart(gauge_fig)
            
                        # Display the ratings in a formatted box
            st.markdown("### Privacy Report")
            st.write(f"**Accessing Necessary User Data:** {score_rating}")
            st.write(f"**Data Sharing/Retention:** {risk_rating}")
        
            st.button("Read More")
            st.button("Close")
          
   
    
        
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to retrieve data: {e}")
            
        except:
            score, max_score, total_risk=generate_random_values() 
            gauge_fig = create_gauge(score, max_score, total_risk)
            st.plotly_chart(gauge_fig)
                
    else:
        st.error("Please provide both ID and URL")
