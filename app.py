import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import base64
import os
from pathlib import Path
import json

# Try to import PIL, but provide a fallback if not available
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Function to get local image path
def get_image_path(type_prefix, index):
    """Get path to local image file based on type and index."""
    assets_dir = Path(__file__).parent / 'assets' / 'images'
    specific_image = assets_dir / f"{type_prefix}{index}.jpeg"
    default_image = assets_dir / "nologo.jpeg"
    
    if specific_image.exists():
        return str(specific_image)
    return str(default_image)

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}],
    assets_folder='assets'
)

# Set the title
app.title = "Joshua Soans - Interactive Resume"

# Define colors
colors = {
    'primary': '#007bff',
    'secondary': '#6c757d',
    'success': '#28a745',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40',
}

# Resume data extracted from LaTeX file in raw-data
personal_info = {
    'name': 'Joshua Soans',
    'location': 'San Francisco',
    'email': 'joshuasoans.13@gmail.com',
    'phone': '+1 919-785-8613',
    'linkedin': 'linkedin.com/in/joshuaneeraj',
    'summary': 'Data Scientist with 7+ years of experience driving business impact through data, advising C-suite executives and senior leadership across industries. Expertise in product analytics, A/B testing, and data engineering, with a proven track record of turning data into actionable insights for diverse stakeholders across Engineering, Product, Finance, and Sales.'
}

experience = [
    {
        'company': 'Amazon',
        'title': 'Business Intelligence Engineer',
        'location': 'Sunnyvale, CA',
        'period': 'Aug. 2021 - Present',
        'image_index': 1,  # Most recent = 1
        'responsibilities': [
            'Driving the growth of FireTV and Alexa\'s multi-million dollar ads business through customer segmentation, bid pricing analytics, and placement optimization models',
            'Designing, executing and analyzing over 100 A/B tests to launch new features, to optimize existing features and to evaluate marketing campaigns with sample sizes averaging 5 million customers',
            'Forecasting customer engagement for over 100 million customers using ensemble methods, including hierarchical reconciliation across multiple dimensions like country and device',
            'Recommending features and devices to customers using both content-based and collaborative filtering methods',
            'Teaching best practices in experimentation, including approaches to minimize pre-test bias, Bayesian versus Frequentist approaches and effective power analysis',
            'Extensive use of SQL, Python, Spark, Redshift, Tableau and most of the AWS data suite'
        ]
    },
    {
        'company': 'Red Hat',
        'title': 'Senior Business Data Scientist',
        'location': 'Raleigh, NC',
        'period': 'May 2018 - Aug. 2021',
        'image_index': 2,
        'responsibilities': [
            'Leading data scientists & engineers in designing dashboards on Tableau Online, providing real-time analytics on over $1.6 billion in annual sales to over 200 sales users',
            'Advising C-suite executives with actionable insights to drive the Sales Strategy for all of Red Hat North America',
            'Leading SQL workshops and other on-the-job training on data tools meant for non-technical colleagues',
            'Designing and maintaining data pipelines using Jupyter Notebooks, Airflow, Redshift and Tableau Online'
        ]
    },
    {
        'company': 'Careerscore',
        'title': 'Analytics Engineering Intern',
        'location': 'Miami, FL',
        'period': 'June 2017 - Aug. 2017',
        'image_index': 3,
        'responsibilities': [
            'Sole analytic engineer at a 5-person startup, building the flagship product\'s recommendation database using Python & SQL to scrape and store web data',
            'Enabling data-driven decisions by mastering visualization tools such as RStudio, Plotly for Python, and Tableau'
        ]
    },
    {
        'company': 'Capillary Technologies',
        'title': 'Technical Account Manager',
        'location': 'Bengaluru, India',
        'period': 'July 2014 - June 2016',
        'image_index': 4,
        'responsibilities': [
            'Leading cross-functional teams involving Engineering, Analytics, Operations and Customer Support to design and implement bespoke loyalty programs, retaining billings averaging over $100,000 annually'
        ]
    }
]

education = [
    {
        'institution': 'North Carolina State University',
        'degree': 'Master of Science in Operations Research',
        'location': 'Raleigh, NC',
        'period': 'Aug. 2016 - May 2018',
        'image_index': 1,
        'details': [
            'Coursework: Design and Analysis of Algorithms, Experimental Statistics for Engineers, Stochastic Models in Industrial Engineering, Linear Programming, Probability Theory & Applications'
        ]
    },
    {
        'institution': 'NIT Karnataka',
        'degree': 'Bachelor of Technology in Mechanical Engineering',
        'location': 'Surathkal, India',
        'period': 'July 2009 - May 2013',
        'image_index': 2,
        'details': []
    }
]

# Load skills from JSON
with open('raw-data/skills.json', 'r') as f:
    skills = json.load(f)

portfolios = {
    'Tableau Portfolio': 'public.tableau.com/profile/joshua.neeraj.soans',
    'Medium Blog': 'medium.com/@joshuaneeraj'
}

# Load and encode images for experience and education
# Add profile photo encoding
profile_photo_path = Path(__file__).parent / 'assets' / 'images' / 'dp.jpeg'
with open(profile_photo_path, 'rb') as f:
    profile_photo = f'data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}'

for exp in experience:
    image_path = get_image_path('experience', exp['image_index'])
    with open(image_path, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode()
        exp['encoded_logo'] = f'data:image/jpeg;base64,{encoded}'

for edu in education:
    image_path = get_image_path('school', edu['image_index'])
    with open(image_path, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode()
        edu['encoded_logo'] = f'data:image/jpeg;base64,{encoded}'

# Create the layout
app.layout = dbc.Container([
    # Header and Summary section in a card
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                # Profile Photo
                dbc.Col([
                    html.Img(src=profile_photo, 
                            style={
                                'height': '100px',
                                'width': '100px',
                                'object-fit': 'cover',
                                'border-radius': '50%',
                                'margin-left': '10px'  # Added margin to move photo right
                            })
                ], width=2, className='pr-0 d-flex align-items-center justify-content-center'),  # Added justify-content-center
                # Name and Contact Info
                dbc.Col([
                    html.H1(personal_info['name'], 
                           className='mb-1', 
                           style={'font-size': '1.5rem', 'font-weight': 'bold', 'color': '#000'}),  # Reduced from 1.8rem to 1.5rem
                    html.Div([
                        html.Span(personal_info['location'], style={'color': '#666'}),
                        html.Span(" | ", style={'color': '#666'}),
                        html.Span(personal_info['email'], style={'color': '#666'}),
                        html.Span(" | ", style={'color': '#666'}),
                        html.Span(personal_info['phone'], style={'color': '#666'}),
                        html.Span(" | ", style={'color': '#666'}),
                        html.A("LinkedIn", href=f"https://{personal_info['linkedin']}", target="_blank")
                    ], style={'font-size': '0.9rem'}),
                    # Summary moved under contact info
                    html.P(personal_info['summary'], 
                          className='mt-2 mb-0',
                          style={'font-size': '0.85rem', 'color': '#333', 'line-height': '1.4'})
                ], width=10, className='pl-3')
            ], className='align-items-start')
        ], className='p-3')
    ], className='mb-2', style={'border': '1px solid #ddd'}),
    
    # Main content - Experience and Skills side by side
    dbc.Row([
        # Left column - Experience and Education
        dbc.Col([
            # Experience Section
            html.H3("Experience", className='mb-2', style={'font-size': '1.1rem', 'font-weight': 'bold'}),
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            # Logo column
                            dbc.Col([
                                html.Img(src=exp['encoded_logo'], 
                                        style={
                                            'height': '40px',
                                            'width': '40px',
                                            'object-fit': 'contain',
                                            'border-radius': '4px',
                                            'margin-left': '8px'
                                        })
                            ], width=1, className='pr-0'),
                            # Content column
                            dbc.Col([
                                # Title and company
                                html.Div([
                                    html.H4(exp['title'], 
                                           className='mb-0', 
                                           style={'font-size': '0.9rem', 'font-weight': 'bold', 'color': '#000'}),
                                    html.H5(exp['company'], 
                                           className='mb-0', 
                                           style={'font-size': '0.85rem', 'color': '#666'})
                                ], className='pl-2'),
                                # Location and period
                                html.P(f"{exp['location']} | {exp['period']}", 
                                      className='mb-1 pl-2',
                                      style={'font-size': '0.75rem', 'color': '#666'}),
                                # Responsibilities
                                html.Ul([
                                    html.Li(resp, style={'font-size': '0.75rem', 'color': '#333', 'line-height': '1.3'}) 
                                    for resp in exp['responsibilities']
                                ], className='mb-0', style={'list-style-type': 'disc', 'padding-left': '16px', 'margin-left': '-16px'})
                            ], width=11)
                        ], className='align-items-start')
                    ], className='py-2')  # Changed from p-2 to py-2 (vertical padding only)
                ], className='mb-2', style={'border': '1px solid #ddd'})
                for exp in experience
            ]),
            
            # Education Section
            html.H3("Education", className='mb-1 mt-3', style={'font-size': '1.1rem', 'font-weight': 'bold'}),  # Added mt-3 to match spacing above Portfolios
            html.Div([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            # Logo column
                            dbc.Col([
                                html.Img(src=edu['encoded_logo'], 
                                        style={
                                            'height': '40px',
                                            'width': '40px',
                                            'object-fit': 'contain',
                                            'border-radius': '4px',
                                            'margin-left': '8px'
                                        })
                            ], width=1, className='pr-0'),
                            # Content column
                            dbc.Col([
                                # Institution and degree
                                html.Div([
                                    html.H4(edu['institution'], 
                                           className='mb-0',
                                           style={'font-size': '0.9rem', 'font-weight': 'bold', 'color': '#000'}),
                                    html.H5(edu['degree'], 
                                           className='mb-0',
                                           style={'font-size': '0.85rem', 'color': '#666'})
                                ], className='pl-2'),
                                # Location and period
                                html.P(f"{edu['location']} | {edu['period']}", 
                                      className='mb-1 pl-2',
                                      style={'font-size': '0.75rem', 'color': '#666'}),
                                # Details if any
                                html.Ul([
                                    html.Li(detail, style={'font-size': '0.75rem', 'color': '#333', 'line-height': '1.3'}) 
                                    for detail in edu['details']
                                ], className='mb-0', style={'list-style-type': 'disc', 'padding-left': '16px', 'margin-left': '-16px'}) if edu['details'] else html.Div()
                            ], width=11)
                        ], className='align-items-start')
                    ], className='py-2')  # Changed from p-2 to py-2 (vertical padding only)
                ], className='mb-2', style={'border': '1px solid #ddd'})
                for edu in education
            ])
        ], width=8, className='pr-2'),
        
        # Right column - Skills and Portfolios
        dbc.Col([
            # Skills Section
            html.H3("Skills", className='mb-2', style={'font-size': '1.1rem', 'font-weight': 'bold'}),
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        dcc.Graph(
                            figure=go.Figure(
                                data=[go.Scatterpolar(
                                    r=list(skills[category].values()) + [list(skills[category].values())[0]],
                                    theta=[label.replace(' & ', '<br>').replace(' and ', '<br>')
                                          .replace('-', '<br>')  # Break hyphenated words
                                          .replace(' ', '<br>')  # Break all spaces for longer labels
                                          if len(label.split()) > 2 or '-' in label  # Apply breaks if more than 2 words or has hyphen
                                          else label.replace(' & ', '<br>').replace(' and ', '<br>')
                                          for label in list(skills[category].keys()) + [list(skills[category].keys())[0]]],
                                    fill='toself',
                                    fillcolor='rgba(255, 0, 0, 0.3)',
                                    line=dict(color='red'),
                                    name=category,
                                    hoverinfo='none',
                                    connectgaps=True
                                )],
                                layout=go.Layout(
                                    polar=dict(
                                        radialaxis=dict(
                                            visible=False,
                                            range=[0, 100],
                                            showline=False,
                                            showgrid=False
                                        ),
                                        angularaxis=dict(
                                            tickfont={'size': 9, 'color': '#000'},
                                            rotation=90,
                                            direction="clockwise",
                                            gridcolor='rgba(0,0,0,0)',
                                            linecolor='rgba(0,0,0,0)',
                                            layer='below traces'
                                        ),
                                        bgcolor='rgba(0,0,0,0)',
                                        domain={'x': [0.1, 0.9], 'y': [0.15, 0.85]}
                                    ),
                                    showlegend=False,
                                    height=180,
                                    margin=dict(l=10, r=10, t=25, b=10),
                                    title=dict(
                                        text=category,
                                        font=dict(size=12, weight='bold', color='#000'),
                                        y=0.98,
                                        x=0,  # Left align the title
                                        xanchor='left'  # Ensure left alignment
                                    ),
                                    paper_bgcolor='rgba(0,0,0,0)',
                                )
                            ),
                            config={'displayModeBar': False},
                            className='mb-2',
                            style={'width': '100%'}
                        )
                    for category in skills.keys()])
                ], className='p-2')
            ], className='mb-3', style={'border': '1px solid #ddd'}),
            
            # Portfolios Section
            html.H3("Portfolios", className='mb-1', style={'font-size': '1.1rem', 'font-weight': 'bold'}),
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Div([
                            html.Span(key, style={'font-size': '0.85rem', 'font-weight': 'bold', 'margin-right': '8px'}),
                            html.A(value, href=f"https://{value}", target="_blank", 
                                  style={'font-size': '0.75rem'})
                        ], className='mb-1') for key, value in portfolios.items()
                    ])
                ], className='p-2')
            ], style={'border': '1px solid #ddd'})
        ], width=4),
    ], className='mb-2'),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Hr(style={'margin': '0.5rem 0'}),
                html.P("Created with Dash and Plotly", 
                      className='mb-0', style={'font-size': '0.65rem'})
            ], className='footer')
        ], width=12)
    ])
], fluid=False, style={'max-width': '1200px', 'margin': '0 auto', 'padding': '15px'})

# Run the app
if __name__ == '__main__':
    app.run(debug=True) 