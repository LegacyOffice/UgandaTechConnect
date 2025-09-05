
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path as MPath
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import textwrap
import warnings

# Check for dependencies
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import numpy as np
    VISUALIZATION_AVAILABLE = True
except ImportError as e:
    print(f"Visualization dependencies missing: {e}. Install 'matplotlib' and 'numpy' to generate diagrams.")
    VISUALIZATION_AVAILABLE = False

# Configuration dictionary for easy customization
CONFIG = {
    "layout": {
        "width": 1200,
        "height": 800,
        "margin": 50,
        "module_width": 200,
        "module_height": 300,
        "module_spacing": 30,
        "platform_width": 140,
        "platform_height": 60,
        "pipeline_width": 1100,
        "pipeline_height": 100,
        "shadow_offset": 5,
        "corner_radius": 0.05
    },
    "typography": {
        "family": ["DejaVu Sans", "Arial", "sans-serif"],
        "title": {"size": 36, "weight": "bold"},
        "subtitle": {"size": 18, "style": "italic"},
        "header": {"size": 20, "weight": "bold"},
        "normal": {"size": 14},
        "small": {"size": 10},
        "tiny": {"size": 8}
    },
    "colors": {
        "background": (240/255, 245/255, 255/255),
        "accent": (50/255, 80/255, 150/255),
        "text": (20/255, 30/255, 60/255),
        "highlight": (255/255, 215/255, 0/255),
        "light_text": (240/255, 240/255, 240/255),
        "shadow": (0/255, 0/255, 0/255, 0.2),
        "modules": [
            (76/255, 175/255, 80/255),   # Curriculum Ingestion - Green
            (33/255, 150/255, 243/255),  # Storyboard - Blue
            (255/255, 152/255, 0/255),   # Asset Creation - Orange
            (156/255, 39/255, 176/255),  # Scene Engine - Purple
            (244/255, 67/255, 54/255)    # Deployment - Red
        ],
        "platforms": (200/255, 230/255, 255/255),
        "pipeline_bg": (220/255, 220/255, 220/255),
        "submodule_bg": (1, 1, 1, 0.9),
        "description_bg": (1, 1, 1, 0.2)
    },
    "output_formats": ["png", "svg", "pdf"]
}

class ColorScheme:
    """Centralized color scheme management"""
    BACKGROUND = CONFIG["colors"]["background"]
    ACCENT = CONFIG["colors"]["accent"]
    TEXT = CONFIG["colors"]["text"]
    HIGHLIGHT = CONFIG["colors"]["highlight"]
    LIGHT_TEXT = CONFIG["colors"]["light_text"]
    SHADOW = CONFIG["colors"]["shadow"]
    MODULES = CONFIG["colors"]["modules"]
    PLATFORMS = CONFIG["colors"]["platforms"]
    PIPELINE_BG = CONFIG["colors"]["pipeline_bg"]
    SUBMODULE_BG = CONFIG["colors"]["submodule_bg"]
    DESCRIPTION_BG = CONFIG["colors"]["description_bg"]

class Typography:
    """Centralized typography settings"""
    FAMILY = CONFIG["typography"]["family"]
    TITLE = CONFIG["typography"]["title"]
    SUBTITLE = CONFIG["typography"]["subtitle"]
    HEADER = CONFIG["typography"]["header"]
    NORMAL = CONFIG["typography"]["normal"]
    SMALL = CONFIG["typography"]["small"]
    TINY = CONFIG["typography"]["tiny"]

class Layout:
    """Centralized layout configuration"""
    WIDTH = CONFIG["layout"]["width"]
    HEIGHT = CONFIG["layout"]["height"]
    MARGIN = CONFIG["layout"]["margin"]
    MODULE_WIDTH = CONFIG["layout"]["module_width"]
    MODULE_HEIGHT = CONFIG["layout"]["module_height"]
    MODULE_SPACING = CONFIG["layout"]["module_spacing"]
    PLATFORM_WIDTH = CONFIG["layout"]["platform_width"]
    PLATFORM_HEIGHT = CONFIG["layout"]["platform_height"]
    PIPELINE_WIDTH = CONFIG["layout"]["pipeline_width"]
    PIPELINE_HEIGHT = CONFIG["layout"]["pipeline_height"]
    SHADOW_OFFSET = CONFIG["layout"]["shadow_offset"]
    CORNER_RADIUS = CONFIG["layout"]["corner_radius"]

class DiagramElement:
    """Base class for all diagram elements"""
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.zorder = 1

    def draw(self, ax):
        raise NotImplementedError("Subclasses must implement draw method")

    def contains_point(self, x: float, y: float) -> bool:
        return (self.x <= x <= self.x + self.width and 
                self.y <= y <= self.y + self.height)

class RoundedBox(DiagramElement):
    """A rounded rectangle element with shadow and optional gradient"""
    def __init__(self, x: float, y: float, width: float, height: float, 
                 facecolor: Tuple, edgecolor: Tuple, linewidth: float = 2,
                 shadow: bool = True, radius: float = Layout.CORNER_RADIUS,
                 gradient: bool = False):
        super().__init__(x, y, width, height)
        self.facecolor = facecolor
        self.edgecolor = edgecolor
        self.linewidth = linewidth
        self.shadow = shadow
        self.radius = radius
        self.gradient = gradient

    def draw(self, ax):
        # Draw shadow if enabled
        if self.shadow:
            shadow = patches.FancyBboxPatch(
                (self.x + Layout.SHADOW_OFFSET, self.y + Layout.SHADOW_OFFSET), 
                self.width, self.height,
                boxstyle=f"round,pad=0.1,rounding_size={self.radius}",
                facecolor=ColorScheme.SHADOW,
                edgecolor='none',
                zorder=self.zorder - 1
            )
            ax.add_patch(shadow)

        # Create gradient if enabled
        if self.gradient:
            gradient_cmap = LinearSegmentedColormap.from_list(
                "custom_gradient", [self.facecolor, (1, 1, 1, 0.9)]
            )
            gradient = np.linspace(0, 1, 256).reshape(1, -1)
            gradient = np.vstack((gradient, gradient))
            ax.imshow(
                gradient, 
                aspect='auto', 
                cmap=gradient_cmap,
                extent=(self.x, self.x + self.width, self.y, self.y + self.height),
                zorder=self.zorder - 0.5,
                alpha=0.3
            )

        # Draw the main box
        box = patches.FancyBboxPatch(
            (self.x, self.y), self.width, self.height,
            boxstyle=f"round,pad=0.1,rounding_size={self.radius}",
            facecolor=self.facecolor if not self.gradient else 'none',
            edgecolor=self.edgecolor,
            linewidth=self.linewidth,
            zorder=self.zorder
        )
        ax.add_patch(box)
        return box

class TextElement(DiagramElement):
    """A text element with formatting options and wrapping"""
    def __init__(self, x: float, y: float, text: str, 
                 fontprops: Dict, color: Tuple, 
                 ha: str = 'center', va: str = 'center',
                 wrap_width: Optional[int] = None):
        super().__init__(x, y, 0, 0)
        self.text = text
        self.fontprops = fontprops
        self.color = color
        self.ha = ha
        self.va = va
        self.wrap_width = wrap_width

    def draw(self, ax):
        # Wrap text if wrap_width is specified
        if self.wrap_width:
            wrapped_text = "\n".join(textwrap.wrap(self.text, self.wrap_width))
        else:
            wrapped_text = self.text

        # Try each font in the family list
        for font in Typography.FAMILY:
            try:
                fontprops = {**self.fontprops, 'family': font}
                text_obj = ax.text(
                    self.x, self.y, wrapped_text,
                    ha=self.ha, va=self.va,
                    color=self.color,
                    **fontprops
                )
                break
            except Exception as e:
                warnings.warn(f"Font '{font}' not available: {e}. Trying next font.")
                continue
        else:
            warnings.warn("No suitable font found. Using default font.")
            text_obj = ax.text(
                self.x, self.y, wrapped_text,
                ha=self.ha, va=self.va,
                color=self.color,
                **self.fontprops
            )

        # Update dimensions based on text size
        renderer = ax.figure.canvas.get_renderer()
        bbox = text_obj.get_window_extent(renderer=renderer)
        bbox = bbox.transformed(ax.transData.inverted())
        self.width = bbox.width
        self.height = bbox.height
        return text_obj

class CurvedArrow(DiagramElement):
    """A curved arrow with improved Bezier curve and customizable style"""
    def __init__(self, start_x: float, start_y: float, end_x: float, end_y: float, 
                 color: Tuple = ColorScheme.ACCENT, width: float = 3, 
                 arrow_size: float = 12, num_dots: int = 3, curve_strength: float = 0.5):
        super().__init__(start_x, start_y, end_x - start_x, end_y - start_y)
        self.end_x = end_x
        self.end_y = end_y
        self.color = color
        self.width = width
        self.arrow_size = arrow_size
        self.num_dots = num_dots
        self.curve_strength = curve_strength
        self.zorder = 3

    def draw(self, ax):
        # Calculate control point for quadratic Bezier curve
        control_x = (self.x + self.end_x) / 2
        control_y = (self.y + self.end_y) / 2 - (self.end_y - self.y) * self.curve_strength

        # Define Bezier curve vertices and codes
        vertices = [
            (self.x, self.y),
            (control_x, control_y),
            (self.end_x, self.end_y)
        ]
        codes = [MPath.MOVETO, MPath.CURVE3, MPath.CURVE3]

        path = MPath(vertices, codes)
        path_patch = patches.PathPatch(
            path, 
            fc="none", 
            ec=self.color, 
            lw=self.width, 
            zorder=self.zorder
        )
        ax.add_patch(path_patch)

        # Draw arrowhead
        t = 0.99  # Position near the end for arrowhead
        dx = (1-t)**2 * vertices[0][0] + 2*(1-t)*t*vertices[1][0] + t**2 * vertices[2][0]
        dy = (1-t)**2 * vertices[0][1] + 2*(1-t)*t*vertices[1][1] + t**2 * vertices[2][1]
        dx_prev = (1-(t-0.01))**2 * vertices[0][0] + 2*(1-(t-0.01))*(t-0.01)*vertices[1][0] + (t-0.01)**2 * vertices[2][0]
        dy_prev = (1-(t-0.01))**2 * vertices[0][1] + 2*(1-(t-0.01))*(t-0.01)*vertices[1][1] + (t-0.01)**2 * vertices[2][1]
        angle = np.arctan2(dy - dy_prev, dx - dx_prev)

        arrow_head = patches.RegularPolygon(
            (self.end_x, self.end_y), 
            numVertices=3, 
            radius=self.arrow_size,
            orientation=angle,
            facecolor=self.color,
            edgecolor='none',
            zorder=self.zorder + 1
        )
        ax.add_patch(arrow_head)

        # Add connecting dots along the curve
        for i in range(1, self.num_dots + 1):
            t = i / (self.num_dots + 1)
            dot_x = (1-t)**2 * vertices[0][0] + 2*(1-t)*t*vertices[1][0] + t**2 * vertices[2][0]
            dot_y = (1-t)**2 * vertices[0][1] + 2*(1-t)*t*vertices[1][1] + t**2 * vertices[2][1]
            dot = patches.Circle(
                (dot_x, dot_y), 4, 
                facecolor=ColorScheme.HIGHLIGHT, 
                edgecolor='none', 
                zorder=self.zorder + 1
            )
            ax.add_patch(dot)
        return path_patch

class Module(DiagramElement):
    """A complete module with title, description, and submodules"""
    def __init__(self, x: float, y: float, width: float, height: float, 
                 title: str, description: str, submodules: List[str], color: Tuple):
        super().__init__(x, y, width, height)
        self.title = title
        self.description = description
        self.submodules = submodules
        self.color = color
        self.elements = []

    def create_elements(self):
        """Create all visual elements for this module"""
        # Main module box with gradient
        main_box = RoundedBox(
            self.x, self.y, self.width, self.height,
            facecolor=self.color,
            edgecolor=ColorScheme.ACCENT,
            linewidth=2,
            gradient=True
        )
        self.elements.append(main_box)

        # Title
        title_text = TextElement(
            self.x + self.width/2, self.y + 30,
            self.title,
            Typography.HEADER,
            ColorScheme.LIGHT_TEXT,
            wrap_width=20
        )
        self.elements.append(title_text)

        # Description background
        desc_bg = RoundedBox(
            self.x + 10, self.y + 50, self.width - 20, 25,
            facecolor=ColorScheme.DESCRIPTION_BG,
            edgecolor='none',
            radius=0.03,
            shadow=False
        )
        self.elements.append(desc_bg)

        # Description text
        desc_text = TextElement(
            self.x + self.width/2, self.y + 62,
            self.description,
            Typography.SMALL,
            ColorScheme.LIGHT_TEXT,
            wrap_width=25
        )
        self.elements.append(desc_text)

        # Submodules
        for i, submodule in enumerate(self.submodules):
            y_pos = self.y + 90 + i * 30
            # Submodule background
            sub_bg = RoundedBox(
                self.x + 10, y_pos, self.width - 20, 25,
                facecolor=ColorScheme.SUBMODULE_BG,
                edgecolor=(180/255, 180/255, 180/255),
                linewidth=1,
                radius=0.03
            )
            self.elements.append(sub_bg)

            # Submodule text
            sub_text = TextElement(
                self.x + 15, y_pos + 12,
                submodule,
                Typography.SMALL,
                (50/255, 50/255, 50/255),
                ha='left', va='center',
                wrap_width=25
            )
            self.elements.append(sub_text)

    def draw(self, ax):
        for element in self.elements:
            element.draw(ax)

class ArchitectureDiagram:
    """Main class for creating system architecture diagrams"""
    def __init__(self, width: int = Layout.WIDTH, height: int = Layout.HEIGHT):
        self.width = width
        self.height = height
        self.elements: List[DiagramElement] = []
        self.modules: List[Module] = []
        self.platforms: List[Dict] = []
        self.ax = None
        self.fig = None

    def setup_canvas(self):
        """Set up the matplotlib canvas"""
        self.fig, self.ax = plt.subplots(figsize=(self.width/100, self.height/100), dpi=100)
        self.fig.set_facecolor(ColorScheme.BACKGROUND)
        self.ax.set_facecolor(ColorScheme.BACKGROUND)
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        self.ax.invert_yaxis()
        self.ax.set_aspect('equal')
        self.ax.axis('off')

    def add_title(self, title: str, subtitle: str = None):
        """Add title and optional subtitle to the diagram"""
        title_element = TextElement(
            self.width/2, 20, title,
            Typography.TITLE,
            ColorScheme.TEXT,
            wrap_width=50
        )
        self.elements.append(title_element)

        if subtitle:
            subtitle_element = TextElement(
                self.width/2, 60, subtitle,
                Typography.SUBTITLE,
                ColorScheme.TEXT,
                wrap_width=50
            )
            self.elements.append(subtitle_element)

    def add_module(self, x: float, y: float, title: str, description: str, 
                  submodules: List[str], color: Tuple) -> Module:
        """Add a module to the diagram"""
        module = Module(x, y, Layout.MODULE_WIDTH, Layout.MODULE_HEIGHT, 
                       title, description, submodules, color)
        module.create_elements()
        self.modules.append(module)
        self.elements.extend(module.elements)
        return module

    def add_arrow(self, start_x: float, start_y: float, end_x: float, end_y: float, 
                  color: Tuple = ColorScheme.ACCENT) -> CurvedArrow:
        """Add an arrow between two points"""
        arrow = CurvedArrow(start_x, start_y, end_x, end_y, color, curve_strength=0.7)
        self.elements.append(arrow)
        return arrow

    def add_platform(self, x: float, y: float, icon: str, text: str):
        """Add a deployment platform"""
        platform_box = RoundedBox(
            x - Layout.PLATFORM_WIDTH/2, y, 
            Layout.PLATFORM_WIDTH, Layout.PLATFORM_HEIGHT,
            facecolor=ColorScheme.PLATFORMS,
            edgecolor=ColorScheme.ACCENT,
            linewidth=2,
            gradient=True
        )
        self.elements.append(platform_box)

        platform_icon = TextElement(
            x, y + 10, icon,
            Typography.NORMAL,
            ColorScheme.TEXT,
            va='top'
        )
        self.elements.append(platform_icon)

        platform_text = TextElement(
            x, y + 40, text,
            {**Typography.SMALL, 'weight': 'bold'},
            ColorScheme.TEXT,
            va='top',
            wrap_width=15
        )
        self.elements.append(platform_text)

        self.platforms.append({
            'x': x, 'y': y, 
            'icon': icon, 'text': text,
            'box': platform_box,
            'icon_element': platform_icon,
            'text_element': platform_text
        })

    def add_footer(self, text: str = None):
        """Add a footer with optional text"""
        if text is None:
            text = f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        footer = TextElement(
            self.width/2, self.height - 20, text,
            {**Typography.SMALL, 'style': 'italic'},
            (ColorScheme.TEXT[0], ColorScheme.TEXT[1], ColorScheme.TEXT[2], 0.7)
        )
        self.elements.append(footer)
        return footer

    def draw(self):
        """Draw all elements on the canvas"""
        for element in self.elements:
            element.draw(self.ax)

    def save(self, filepath: str):
        """Save the diagram to multiple formats"""
        filepath = Path(filepath)
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        for fmt in CONFIG["output_formats"]:
            try:
                output_path = filepath.with_suffix(f".{fmt}")
                plt.savefig(output_path, bbox_inches='tight', dpi=300, facecolor=ColorScheme.BACKGROUND)
                print(f"Diagram saved to {output_path}")
            except Exception as e:
                print(f"Failed to save diagram as {fmt}: {e}")
        plt.close()

    def create_system_architecture(self, filepath: str):
        """Create a complete system architecture diagram"""
        self.setup_canvas()

        self.add_title(
            "System Architecture", 
            "Interactive Educational Content Pipeline"
        )

        module_definitions = [
            {
                "title": "Curriculum Ingestion", 
                "desc": "Upload and parse CBC documents for learning objectives", 
                "submodules": ["PDF Parser", "Objective Extractor", "Curriculum Tagger"],
                "color": ColorScheme.MODULES[0]
            },
            {
                "title": "Storyboard & Scripting", 
                "desc": "Design pedagogical flow and interactive elements", 
                "submodules": ["Visual Editor", "JSON Generator", "Interactive Points"],
                "color": ColorScheme.MODULES[1]
            },
            {
                "title": "Asset Creation", 
                "desc": "Create and manage 3D models, images, and AI content", 
                "submodules": ["3D Model Library", "AI Image Generator", "ControlNet Integration"],
                "color": ColorScheme.MODULES[2]
            },
            {
                "title": "Scene Engine", 
                "desc": "Assemble interactive lessons with Unity", 
                "submodules": ["Unity Runtime", "C# Scripts", "URP Renderer"],
                "color": ColorScheme.MODULES[3]
            },
            {
                "title": "Deployment", 
                "desc": "Compile and export lessons to platforms", 
                "submodules": ["SCORM Packager", "WebGL Exporter", "APK Builder"],
                "color": ColorScheme.MODULES[4]
            }
        ]

        # Dynamic module positioning
        num_modules = len(module_definitions)
        total_width = num_modules * Layout.MODULE_WIDTH + (num_modules - 1) * Layout.MODULE_SPACING
        start_x = (self.width - total_width) / 2
        modules = []
        for i, module_def in enumerate(module_definitions):
            x = start_x + i * (Layout.MODULE_WIDTH + Layout.MODULE_SPACING)
            y = 150
            module = self.add_module(
                x, y, 
                module_def["title"], 
                module_def["desc"], 
                module_def["submodules"], 
                module_def["color"]
            )
            modules.append(module)

        # Add arrows between modules
        for i in range(len(modules) - 1):
            start_x = modules[i].x + modules[i].width
            start_y = modules[i].y + modules[i].height/2
            end_x = modules[i+1].x
            end_y = modules[i+1].y + modules[i+1].height/2
            self.add_arrow(start_x, start_y, end_x, end_y)

        # Add deployment targets label
        targets_label = TextElement(
            self.width/2, 520, "Deployment Targets",
            {**Typography.HEADER, 'weight': 'bold'},
            ColorScheme.TEXT
        )
        self.elements.append(targets_label)

        # Add platforms
        platforms = [
            {"icon": "📚", "text": "Kolibri (SCORM)"},
            {"icon": "🌐", "text": "Web Browsers (WebGL)"},
            {"icon": "📱", "text": "Android (APK)"}
        ]

        num_platforms = len(platforms)
        platform_spacing = 300
        total_platform_width = num_platforms * platform_spacing
        start_x_platforms = (self.width - total_platform_width + platform_spacing) / 2
        for i, platform in enumerate(platforms):
            x = start_x_platforms + i * platform_spacing
            y = 580
            self.add_platform(x, y, platform["icon"], platform["text"])

            # Add arrow from deployment module to platform
            deployment_module = modules[-1]
            arrow_start_x = deployment_module.x + deployment_module.width/2
            arrow_start_y = deployment_module.y + deployment_module.height
            arrow_end_x = x
            arrow_end_y = y
            self.add_arrow(
                arrow_start_x, arrow_start_y, 
                arrow_end_x, arrow_end_y, 
                ColorScheme.MODULES[4]
            )

        self.add_footer()
        self.draw()
        self.save(filepath)

class PipelineDiagram(ArchitectureDiagram):
    """Specialized diagram for graphics pipeline visualization"""
    def create_graphics_pipeline(self, filepath: str):
        """Create a graphics pipeline diagram"""
        self.setup_canvas()

        self.add_title(
            "Graphics and Content Pipeline", 
            "From Concept to Deployed Educational Content"
        )

        pipeline_x = (self.width - Layout.PIPELINE_WIDTH) / 2
        pipeline_y = 500

        pipeline_bg = RoundedBox(
            pipeline_x, pipeline_y, 
            Layout.PIPELINE_WIDTH, Layout.PIPELINE_HEIGHT,
            facecolor=ColorScheme.PIPELINE_BG,
            edgecolor=(180/255, 180/255, 180/255),
            linewidth=2,
            gradient=True
        )
        self.elements.append(pipeline_bg)

        stages = [
            {"name": "Pre-visualization", "icon": "✏️", "color": ColorScheme.MODULES[1]},
            {"name": "3D Asset Creation", "icon": "🛠️", "color": ColorScheme.MODULES[2]},
            {"name": "Scene Assembly", "icon": "🧩", "color": ColorScheme.MODULES[3]},
            {"name": "Rendering & Optimization", "icon": "🎨", "color": ColorScheme.MODULES[4]}
        ]

        stage_width = Layout.PIPELINE_WIDTH / len(stages)
        for i, stage in enumerate(stages):
            x_pos = pipeline_x + i * stage_width

            if i > 0:
                line = patches.ConnectionPatch(
                    (x_pos, pipeline_y), (x_pos, pipeline_y + Layout.PIPELINE_HEIGHT),
                    coordsA='data', coordsB='data',
                    color=(150/255, 150/255, 150/255),
                    linewidth=2,
                    linestyle=':'
                )
                self.ax.add_patch(line)

            stage_label = TextElement(
                x_pos + stage_width/2, pipeline_y + Layout.PIPELINE_HEIGHT/2 + 10,
                stage["name"],
                {**Typography.NORMAL, 'weight': 'bold'},
                ColorScheme.TEXT,
                wrap_width=15
            )
            self.elements.append(stage_label)

            icon_bg = patches.Circle(
                (x_pos + stage_width/2, pipeline_y + Layout.PIPELINE_HEIGHT/2 - 15), 
                20,
                facecolor=(1, 1, 1, 0.7),
                edgecolor=(150/255, 150/255, 150/255),
                linewidth=1,
                zorder=2
            )
            self.ax.add_patch(icon_bg)

            stage_icon = TextElement(
                x_pos + stage_width/2, pipeline_y + Layout.PIPELINE_HEIGHT/2 - 15,
                stage["icon"],
                Typography.NORMAL,
                ColorScheme.TEXT
            )
            self.elements.append(stage_icon)

            stage_num = TextElement(
                x_pos + stage_width/2, pipeline_y - 40,
                f"Step {i+1}",
                {**Typography.SMALL, 'weight': 'bold'},
                stage["color"]
            )
            self.elements.append(stage_num)

            if i < len(stages) - 1:
                arrow_start_x = x_pos + stage_width - 10
                arrow_start_y = pipeline_y + Layout.PIPELINE_HEIGHT/2
                arrow_end_x = x_pos + stage_width + 10
                arrow_end_y = pipeline_y + Layout.PIPELINE_HEIGHT/2
                self.add_arrow(arrow_start_x, arrow_start_y, arrow_end_x, arrow_end_y)

        process_steps = [
            "Storyboard creation and script development",
            "3D modeling and asset preparation",
            "Scene composition and interactive elements",
            "Optimization for target platforms"
        ]

        for i, step in enumerate(process_steps):
            y_pos = pipeline_y + Layout.PIPELINE_HEIGHT + 60 + i * 30
            bullet = TextElement(
                pipeline_x + 20, y_pos, "•",
                Typography.NORMAL,
                ColorScheme.MODULES[i]
            )
            self.elements.append(bullet)

            step_text = TextElement(
                pipeline_x + 40, y_pos, step,
                Typography.SMALL,
                ColorScheme.TEXT,
                ha='left',
                wrap_width=50
            )
            self.elements.append(step_text)

        self.add_footer()
        self.draw()
        self.save(filepath)

def main():
    """Main function to generate all diagrams"""
    if not VISUALIZATION_AVAILABLE:
        print("Visualization skipped due to missing dependencies. Install matplotlib and numpy.")
        return

    date_str = datetime.now().strftime("%Y%m%d")
    try:
        arch_diagram = ArchitectureDiagram()
        arch_diagram.create_system_architecture(f"screenshots/architecture_{date_str}")
        pipeline_diagram = PipelineDiagram()
        pipeline_diagram.create_graphics_pipeline(f"screenshots/pipeline_{date_str}")
        print("Diagrams generated successfully!")
        print(f"Check the 'screenshots' directory for output files.")
    except Exception as e:
        print(f"Error generating diagrams: {e}")

if __name__ == "__main__":
    main()
