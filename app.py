import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import base64
from pathlib import Path
import json

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def get_image_path(type_prefix, index):
    """Get path to local image file based on type and index."""
    assets_dir = Path(__file__).parent / 'assets' / 'images'
    specific_image = assets_dir / f"{type_prefix}{index}.jpeg"
    default_image = assets_dir / "nologo.jpeg"
    if specific_image.exists():
        return str(specific_image)
    return str(default_image)


# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------
ACCENT = '#C45A3C'
ACCENT_FILL = 'rgba(196, 90, 60, 0.15)'
TEXT = '#1A1A1A'
TEXT_SEC = '#5C5C5C'
TEXT_MUTED = '#8C8C8C'
BORDER = '#E8E5E0'
SURFACE = '#FFFFFF'
BG = '#F9F8F6'

# ---------------------------------------------------------------------------
# App initialization
# ---------------------------------------------------------------------------
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
    ],
    meta_tags=[
        {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'},
    ],
    assets_folder='assets',
    title='Joshua Soans — Resume',
)

server = app.server
app.title = 'Joshua Soans — Interactive Resume'

# ---------------------------------------------------------------------------
# Resume data
# ---------------------------------------------------------------------------
personal_info = {
    'name': 'Joshua Soans',
    'location': 'San Francisco',
    'email': 'joshuasoans.13@gmail.com',
    'phone': '+1 919-785-8613',
    'linkedin': 'linkedin.com/in/joshuaneeraj',
    'summary': (
        'Data Scientist with 7+ years of experience driving business impact '
        'through data, advising C-suite executives and senior leadership across '
        'industries. Expertise in product analytics, A/B testing, and data '
        'engineering, with a proven track record of turning data into actionable '
        'insights for diverse stakeholders across Engineering, Product, Finance, '
        'and Sales.'
    ),
}

experience = [
    {
        'company': 'Amazon',
        'title': 'Business Intelligence Engineer',
        'location': 'Sunnyvale, CA',
        'period': 'Aug 2021 — Present',
        'image_index': 1,
        'responsibilities': [
            "Driving the growth of FireTV and Alexa's multi-million dollar ads business through customer segmentation, bid pricing analytics, and placement optimization models",
            'Designing, executing and analyzing over 100 A/B tests to launch new features, to optimize existing features and to evaluate marketing campaigns with sample sizes averaging 5 million customers',
            'Forecasting customer engagement for over 100 million customers using ensemble methods, including hierarchical reconciliation across multiple dimensions like country and device',
            'Recommending features and devices to customers using both content-based and collaborative filtering methods',
            'Teaching best practices in experimentation, including approaches to minimize pre-test bias, Bayesian versus Frequentist approaches and effective power analysis',
            'Extensive use of SQL, Python, Spark, Redshift, Tableau and most of the AWS data suite',
        ],
    },
    {
        'company': 'Red Hat',
        'title': 'Senior Business Data Scientist',
        'location': 'Raleigh, NC',
        'period': 'May 2018 — Aug 2021',
        'image_index': 2,
        'responsibilities': [
            'Leading data scientists & engineers in designing dashboards on Tableau Online, providing real-time analytics on over $1.6 billion in annual sales to over 200 sales users',
            'Advising C-suite executives with actionable insights to drive the Sales Strategy for all of Red Hat North America',
            'Leading SQL workshops and other on-the-job training on data tools meant for non-technical colleagues',
            'Designing and maintaining data pipelines using Jupyter Notebooks, Airflow, Redshift and Tableau Online',
        ],
    },
    {
        'company': 'Careerscore',
        'title': 'Analytics Engineering Intern',
        'location': 'Miami, FL',
        'period': 'Jun 2017 — Aug 2017',
        'image_index': 3,
        'responsibilities': [
            "Sole analytic engineer at a 5-person startup, building the flagship product's recommendation database using Python & SQL to scrape and store web data",
            'Enabling data-driven decisions by mastering visualization tools such as RStudio, Plotly for Python, and Tableau',
        ],
    },
    {
        'company': 'Capillary Technologies',
        'title': 'Technical Account Manager',
        'location': 'Bengaluru, India',
        'period': 'Jul 2014 — Jun 2016',
        'image_index': 4,
        'responsibilities': [
            'Leading cross-functional teams involving Engineering, Analytics, Operations and Customer Support to design and implement bespoke loyalty programs, retaining billings averaging over $100,000 annually',
        ],
    },
]

education = [
    {
        'institution': 'North Carolina State University',
        'degree': 'Master of Science in Operations Research',
        'location': 'Raleigh, NC',
        'period': 'Aug 2016 — May 2018',
        'image_index': 1,
        'details': [
            'Coursework: Design and Analysis of Algorithms, Experimental Statistics for Engineers, Stochastic Models in Industrial Engineering, Linear Programming, Probability Theory & Applications',
        ],
    },
    {
        'institution': 'NIT Karnataka',
        'degree': 'Bachelor of Technology in Mechanical Engineering',
        'location': 'Surathkal, India',
        'period': 'Jul 2009 — May 2013',
        'image_index': 2,
        'details': [],
    },
]

with open('raw-data/skills.json', 'r') as f:
    skills = json.load(f)

portfolios = {
    'Tableau Portfolio': 'public.tableau.com/profile/joshua.neeraj.soans',
    'Medium Blog': 'medium.com/@joshuaneeraj',
}

# ---------------------------------------------------------------------------
# Encode images
# ---------------------------------------------------------------------------
profile_photo_path = Path(__file__).parent / 'assets' / 'images' / 'dp.jpeg'
with open(profile_photo_path, 'rb') as f:
    profile_photo = f'data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}'

for exp in experience:
    path = get_image_path('experience', exp['image_index'])
    with open(path, 'rb') as f:
        exp['encoded_logo'] = f'data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}'

for edu in education:
    path = get_image_path('school', edu['image_index'])
    with open(path, 'rb') as f:
        edu['encoded_logo'] = f'data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}'


# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------
def section_heading(text):
    """Render an uppercase section label with an accent underline."""
    return html.Div(
        html.Span(text, className='section-title'),
        className='mb-3',
    )


def experience_card(exp):
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Img(src=exp['encoded_logo'], style={
                        'height': '36px', 'width': '36px',
                        'object-fit': 'contain', 'border-radius': '8px',
                        'border': f'1px solid {BORDER}',
                        'padding': '4px', 'background': SURFACE,
                    })
                ], width='auto', className='d-flex align-items-start pe-2'),
                dbc.Col([
                    html.Div(exp['title'], style={
                        'font-size': '0.9rem', 'font-weight': '600',
                        'color': TEXT, 'line-height': '1.3',
                    }),
                    html.Div(exp['company'], style={
                        'font-size': '0.82rem', 'color': TEXT_SEC,
                        'line-height': '1.3',
                    }),
                    html.Div(
                        f"{exp['location']}  ·  {exp['period']}",
                        style={
                            'font-size': '0.75rem', 'color': TEXT_MUTED,
                            'margin-top': '2px', 'margin-bottom': '8px',
                        },
                    ),
                    html.Ul(
                        [html.Li(r, style={
                            'font-size': '0.78rem', 'color': TEXT_SEC,
                            'line-height': '1.5', 'margin-bottom': '4px',
                        }) for r in exp['responsibilities']],
                        style={
                            'padding-left': '16px', 'margin-bottom': '0',
                            'list-style-type': 'disc',
                        },
                    ),
                ]),
            ], className='g-0'),
        ], className='p-3'),
    ], className='mb-2')


def education_card(edu):
    children = [
        html.Div(edu['institution'], style={
            'font-size': '0.9rem', 'font-weight': '600', 'color': TEXT,
        }),
        html.Div(edu['degree'], style={
            'font-size': '0.82rem', 'color': TEXT_SEC,
        }),
        html.Div(
            f"{edu['location']}  ·  {edu['period']}",
            style={
                'font-size': '0.75rem', 'color': TEXT_MUTED,
                'margin-top': '2px',
            },
        ),
    ]
    if edu['details']:
        children.append(
            html.Ul(
                [html.Li(d, style={
                    'font-size': '0.78rem', 'color': TEXT_SEC,
                    'line-height': '1.5',
                }) for d in edu['details']],
                style={
                    'padding-left': '16px', 'margin-bottom': '0',
                    'margin-top': '6px', 'list-style-type': 'disc',
                },
            )
        )

    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Img(src=edu['encoded_logo'], style={
                        'height': '36px', 'width': '36px',
                        'object-fit': 'contain', 'border-radius': '8px',
                        'border': f'1px solid {BORDER}',
                        'padding': '4px', 'background': SURFACE,
                    })
                ], width='auto', className='d-flex align-items-start pe-2'),
                dbc.Col(children),
            ], className='g-0'),
        ], className='p-3'),
    ], className='mb-2')


def skills_chart(category, data):
    """Build a Plotly radar chart for one skill category."""
    labels = list(data.keys())
    values = list(data.values())
    labels_closed = labels + [labels[0]]
    values_closed = values + [values[0]]

    # Wrap long labels for readability
    wrapped = []
    for label in labels_closed:
        if len(label.split()) > 2 or '-' in label:
            wrapped.append(
                label.replace(' & ', '<br>').replace(' and ', '<br>')
                     .replace('-', '<br>').replace(' ', '<br>')
            )
        else:
            wrapped.append(
                label.replace(' & ', '<br>').replace(' and ', '<br>')
            )

    fig = go.Figure(data=[go.Scatterpolar(
        r=values_closed,
        theta=wrapped,
        fill='toself',
        fillcolor=ACCENT_FILL,
        line=dict(color=ACCENT, width=2),
        hoverinfo='none',
        connectgaps=True,
    )])

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False, range=[0, 100],
                showline=False, showgrid=False,
            ),
            angularaxis=dict(
                tickfont={'size': 9, 'color': TEXT_SEC, 'family': 'Inter, sans-serif'},
                rotation=90, direction='clockwise',
                gridcolor='rgba(0,0,0,0)', linecolor='rgba(0,0,0,0)',
                layer='below traces',
            ),
            bgcolor='rgba(0,0,0,0)',
            domain={'x': [0.1, 0.9], 'y': [0.15, 0.85]},
        ),
        showlegend=False,
        height=190,
        margin=dict(l=10, r=10, t=30, b=10),
        title=dict(
            text=f'<b>{category}</b>',
            font=dict(size=12, color=TEXT, family='Inter, sans-serif'),
            y=0.98, x=0, xanchor='left',
        ),
        paper_bgcolor='rgba(0,0,0,0)',
    )

    return dcc.Graph(
        figure=fig,
        config={'displayModeBar': False},
        className='mb-1',
        style={'width': '100%'},
    )


# ---------------------------------------------------------------------------
# Page layout
# ---------------------------------------------------------------------------
app.layout = dbc.Container([

    # --- Header -----------------------------------------------------------
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Img(src=profile_photo, style={
                    'height': '88px', 'width': '88px',
                    'object-fit': 'cover', 'border-radius': '50%',
                    'border': f'3px solid {BORDER}',
                })
            ], width='auto', className='d-flex align-items-center pe-3'),

            dbc.Col([
                html.H1(personal_info['name'], style={
                    'font-size': '1.5rem', 'font-weight': '700',
                    'color': TEXT, 'margin-bottom': '4px',
                    'letter-spacing': '-0.01em',
                }),
                html.Div([
                    html.Span(personal_info['location'],
                              style={'color': TEXT_SEC}),
                    html.Span(' · ',
                              style={'color': TEXT_MUTED, 'margin': '0 6px'}),
                    html.Span(personal_info['email'],
                              style={'color': TEXT_SEC}),
                    html.Span(' · ',
                              style={'color': TEXT_MUTED, 'margin': '0 6px'}),
                    html.Span(personal_info['phone'],
                              style={'color': TEXT_SEC}),
                    html.Span(' · ',
                              style={'color': TEXT_MUTED, 'margin': '0 6px'}),
                    html.A('LinkedIn',
                           href=f"https://{personal_info['linkedin']}",
                           target='_blank',
                           style={'font-weight': '500'}),
                ], style={'font-size': '0.85rem', 'margin-bottom': '10px'}),
                html.P(personal_info['summary'], style={
                    'font-size': '0.85rem', 'color': TEXT_SEC,
                    'line-height': '1.55', 'margin-bottom': '0',
                }),
            ]),
        ], className='g-0'),
    ], className='mb-4 p-4', style={
        'background': SURFACE, 'border-radius': '16px',
        'border': f'1px solid {BORDER}',
        'box-shadow': '0 1px 3px rgba(0,0,0,0.04)',
    }),

    # --- Main content -----------------------------------------------------
    dbc.Row([

        # Left column — Experience + Education
        dbc.Col([
            section_heading('Experience'),
            html.Div([experience_card(exp) for exp in experience]),
            html.Div(style={'height': '24px'}),
            section_heading('Education'),
            html.Div([education_card(edu) for edu in education]),
        ], lg=8, md=12, className='pe-lg-3'),

        # Right column — Skills + Portfolios
        dbc.Col([
            section_heading('Skills'),
            dbc.Card([
                dbc.CardBody([
                    skills_chart(cat, data)
                    for cat, data in skills.items()
                ], className='p-2'),
            ], className='mb-3'),

            html.Div(style={'height': '8px'}),

            section_heading('Portfolios'),
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.A(key, href=f'https://{value}', target='_blank',
                               style={'font-size': '0.85rem', 'font-weight': '500'}),
                    ], className='mb-2')
                    for key, value in portfolios.items()
                ], className='p-3'),
            ]),
        ], lg=4, md=12),

    ], className='g-0'),

    # --- Footer -----------------------------------------------------------
    html.Div([
        html.Hr(style={'border-color': BORDER, 'margin': '24px 0 12px'}),
        html.P(
            'Built with Dash & Plotly',
            style={
                'font-size': '0.7rem', 'color': TEXT_MUTED,
                'text-align': 'center', 'margin-bottom': '0',
            },
        ),
    ]),

], fluid=False, style={
    'max-width': '1100px', 'margin': '0 auto', 'padding': '24px 16px',
})


if __name__ == '__main__':
    app.run(debug=True)
