"""
A CNN theme for Altair.
"""
# Color schemes and defaults
palette = dict(
    black="#c00",
    white="#ffffff",
    default="#9e79c0",
    accent="#7c4ea5",
    highlight="#21594E",
    # politics
    democrat="#5194c3",
    republican="#c52622",
    third_party="#F8C153",
    green_party="#53A796",
    # gender
    women="#7C4EA5",
    men="#F8C153",
    nonbinary="#E6655A",
    # demographics
    demo_american_indian="#F8C153",
    demo_asian="#01446D",
    demo_black="#F18851",
    demo_hispanic="#5194C3",
    demo_multiracial="#53A796",
    demo_pacific_islander="#7C4EA5",
    demo_other_race="#B1B1B1",
    demo_white="#BBE6F8",
    schemes={
        "purples": [
            '#e2d7ec', '#c0a8d6', '#9e79c0', '#7c4ea5', '#593876'
        ],
        "category-5": [
            "#7c4ea5",
            "#5194c3",
            "#f8c153",
            "#53a796",
            "#f18851",
        ],
        "teal-7": [
            "#C7EAE5",
            "#A6CDC7",
            "#85B0A9",
            "#64938B",
            "#42766C",
            "#21594E",
            "#003C30"
        ],
        "fireandice-6": [
            "#e68a4f",
            "#f4bb6a",
            "#f9e39c",
            "#dadfe2",
            "#a6b7c6",
            "#849eae",
        ],
        "ice-7": [
            "#edefee",
            "#dadfe2",
            "#c4ccd2",
            "#a6b7c6",
            "#849eae",
            "#607785",
            "#47525d",
        ],
        "cb-diverging-purpgrn": [
            "#762a83",
            "#af8dc3",
            "#e7d4e8",
            "#f7f7f7",
            "#d9f0d3",
            "#7fbf7b",
            "#1b7837",
        ],
        "cb-diverging-bluegreen": [
            "#8c510a",
            "#d8b365",
            "#f6e8c3",
            "#f5f5f5",
            "#c7eae5",
            "#5ab4ac",
            "#01665e",
        ],
        # Political ramps
        "rep_ramp": [
            "#ffd3c3",
            "#f89a8b",
            "#E6655A",
            "#c52622",
            "#9a040b",
            "#670000"
        ],
        "dem_ramp": [
            "#BBE6F8",
            "#8CC8F6",
            "#5194C3",
            "#166296",
            "#01446D",
            "#042853"
        ],
        "yellow-red": [
            "#ffffb2",
            "#fecc5c",
            "#fd8d3c",
            "#f03b20",
            "#bd0026"
        ]
    }
)

def theme():
    """
    A CNN theme for Altair.
    """
    # Headlines
    headlineFontSize = 18
    headlineFontWeight = "bold"
    headlineFont = "CNNSansDisplay-Bold"

    # Titles for axes and legends
    titleFont = "CNN Sans Display"
    titleFontWeight = "bold"
    titleFontSize = 12
    titleFontSizeLegend = 14
    titleFontSizeY = 15
    titleFontColor = '#262626'

    # Labels for ticks and legend entries
    labelFont = "CNN Sans Display"
    labelFontSize = 12
    labelFontWeight = "normal"

    # Etc
    axisGridColor = "#ececec"
    axisTitleColor = '#262626'
    axisDomainColor = '#ececec'
    axisLabelColor = '#b1b1b1'
    axisTickColor = '#b1b1b1'

    return dict(
        config=dict(
            padding={"left": 0, "top": 10, "right": 5, "bottom": 0},
            view=dict(width=650, height=400, strokeOpacity=0),
            background=palette["white"],
            title=dict(
                anchor="start",
                font=headlineFont,
                fontColor=titleFontColor,
                fontSize=headlineFontSize,
                fontWeight=headlineFontWeight,
                dy=-10,
                dx=10
            ),
            arc=dict(fill=palette["default"]),
            area=dict(fill=palette["default"], opacity=.6),
            line=dict(stroke=palette["default"], strokeWidth=3),
            path=dict(stroke=palette["default"]),
            rect=dict(fill=palette["default"]),
            shape=dict(stroke=palette["default"]),
            bar=dict(fill=palette["default"]),
            point=dict(stroke=palette["default"]),
            symbol=dict(fill=palette["default"], size=30),
            axis=dict(
                titleFont=titleFont,
                titleFontSize=titleFontSize,
                titleFontWeight=titleFontWeight,
                labelFont=labelFont,
                labelFontSize=labelFontSize,
                labelFontWeight=labelFontWeight,
                tickColor=axisTickColor,
                domainColor=axisDomainColor
            ),
            axisX=dict(
                labelAngle=0, 
                labelPadding=10, 
                tickSize=2, 
                grid=False,
                gridColor=axisGridColor,
                titleColor=axisTitleColor,
                labelColor=axisLabelColor
            ),
            axisY=dict(
                labelBaseline="middle",
                maxExtent=45,
                minExtent=45,
                titleAlign="left",
                titleAngle=0,
                titleX=-35,
                titleY=-46,
                domainOpacity=0,
                gridWidth=0.6,
                gridColor=axisGridColor,
                offset=15,
                tickSize=0,
                titleColor=axisTitleColor,
                titleFontWeight=titleFontWeight,
                titleFontSize=titleFontSizeY,
                labelColor=axisLabelColor
            ),
            legend=dict(
                titleFont=titleFont,
                titleFontSize=titleFontSizeLegend,
                titleFontWeight=titleFontWeight,
                symbolType="square",
                orient='top',
                labelFont=labelFont,
                labelFontSize=labelFontSize,
                anchor='middle',
                legendX=0
            ),
            range=dict(
                category=palette["schemes"]["category-5"],
                diverging=palette["schemes"]["cb-diverging-bluegreen"],
                heatmap=palette["schemes"]["yellow-red"],
                ordinal=palette["schemes"]["category-5"],
                ramp=palette["schemes"]["purples"],
            ),
            text=dict(
                font=labelFont,
                color=axisLabelColor,
                fontSize=labelFontSize,
                fontWeight="normal",  
                align="center",  
                baseline="middle"
            )
        )
    )
