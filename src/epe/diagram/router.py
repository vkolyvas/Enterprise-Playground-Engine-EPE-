"""Diagram router — selects the appropriate MCP server based on diagram type.

Router logic:
  - Azure/cloud architecture → Azure-DrawIO-MCP (azure diagram)
  - Full programmatic control (shapes, pages, layers) → lgazo/drawio-mcp-server (server)
  - Simple flows, inline renders, general architecture → jgraph/drawio-mcp (drawio)

Usage:
    from epe.diagram.router import DiagramRouter, DiagramType

    router = DiagramRouter()
    result = router.render(
        diagram_type=DiagramType.LIFECYCLE_FLOW,
        project_id="number2",
        output_path="docs/diagrams/lifecycle.drawio"
    )
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Diagram types
# ---------------------------------------------------------------------------


class DiagramType(Enum):
    # jgraph/drawio-mcp — inline render, simple flows
    LIFECYCLE_FLOW = "lifecycle_flow"  # product → presales → architecture → delivery
    STAGE_GATE = "stage_gate"  # gate predicates and transitions
    TRACEABILITY_SPINE = "traceability_spine"  # CUST → REQ → COMP → DEC → TEST → EVD
    DATA_FLOW = "data_flow"  # document flow between stages

    # lgazo/drawio-mcp-server — programmatic control
    COMPONENT_MAP = "component_map"  # Tele-MANAS 15 components with relationships
    ENTITY_GRAPH = "entity_graph"  # REQ/COMP/DEC/TASK relationships

    # Azure-DrawIO-MCP — Azure architecture
    AZURE_ARCH = "azure_arch"  # Azure components (App Service, SQL, etc.)


# ---------------------------------------------------------------------------
# MCP server identifiers
# ---------------------------------------------------------------------------


class MCPServer(Enum):
    DRAWIO = "drawio"  # jgraph/drawio-mcp — inline rendering
    SERVER = "server"  # lgazo/drawio-mcp-server — full programmatic
    AZURE = "azure"  # Azure-DrawIO-MCP — Azure architectures


# ---------------------------------------------------------------------------
# Router decision logic
# ---------------------------------------------------------------------------

# Azure resource indicators — auto-detected in architecture content
AZURE_INDICATORS = {
    "azure", "aws", "gcp", "app service", "azure sql", "azure blob",
    "azure functions", "azure kubernetes", "aks", "azure devops",
    "azure active directory", "azure ad", "azure monitor", "azure app insights",
    "azure storage", "azure cosmos db", "azure redis", "azure cdn",
    "azure firewall", "azure load balancer", "azure application gateway",
    "app service", "functions", "azure resource", "azure cloud",
}


def detect_cloud_provider(content: str) -> MCPServer | None:
    """Auto-detect cloud provider from content analysis."""
    lower = content.lower()
    if any(ind in lower for ind in AZURE_INDICATORS):
        return MCPServer.AZURE
    return None


def route(diagram_type: DiagramType, content: str = "", inline: bool = False) -> MCPServer:
    """Select the appropriate MCP server for the given diagram.

    Decision tree:
      1. If inline=True or simple flow → jgraph/drawio-mcp (inline render)
      2. If auto-detected Azure content → Azure-DrawIO-MCP
      3. If COMPONENT_MAP or ENTITY_GRAPH (complex, many entities) →
         lgazo/drawio-mcp-server (full programmatic control)
      4. Default → jgraph/drawio-mcp

    Args:
        diagram_type: Type of diagram to render
        content: Optional content to analyze for cloud provider detection
        inline: If True, prefer inline rendering (jgraph/drawio-mcp)
    """
    # 1. Inline rendering preference
    if inline or diagram_type in {
        DiagramType.LIFECYCLE_FLOW,
        DiagramType.STAGE_GATE,
        DiagramType.DATA_FLOW,
    }:
        return MCPServer.DRAWIO

    # 2. Azure auto-detection
    cloud = detect_cloud_provider(content)
    if cloud == MCPServer.AZURE or diagram_type == DiagramType.AZURE_ARCH:
        return MCPServer.AZURE

    # 3. Complex diagrams needing full programmatic control
    if diagram_type in {
        DiagramType.COMPONENT_MAP,
        DiagramType.ENTITY_GRAPH,
    }:
        return MCPServer.SERVER

    # 4. Default: inline rendering
    return MCPServer.DRAWIO


# ---------------------------------------------------------------------------
# Diagram templates (draw.io XML)
# ---------------------------------------------------------------------------

# Standard draw.io namespace
DRAWIO_NS = "http://draw.io"


def _mx(tag: str, attribs: dict[str, str] | None = None, text: str | None = None) -> ET.Element:
    el = ET.Element(f"mxCell/{tag}" if "/" in tag else tag, attribs or {})
    if text is not None:
        el.text = text
    return el


def _cell(id: str, parent: str = "0", style: str = "", value: str = "", **kw) -> ET.Element:
    attribs = {
        "id": id,
        "parent": parent,
        "style": style,
        "value": value,
    }
    attribs.update({k: str(v) for k, v in kw.items()})
    return ET.Element("mxCell", attribs)


# ---------------------------------------------------------------------------
# Lifecycle Flow diagram (product → presales → architecture → delivery)
# ---------------------------------------------------------------------------

LIFECYCLE_STYLES = {
    "stage": "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=14",
    "gate": "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=12",
    "artifact": "rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=10;dashed=1",
    "handover": "endArrow=classic;html=1;strokeWidth=2;strokeColor=#6c8ebf",
    "edge": "endArrow=block;html=1;strokeWidth=1;strokeColor=#666666;dashed=1",
}

LIFECYCLE_LAYOUT = [
    # (id, type, label, x, y)
    ("1", "stage", "PRODUCT", 80, 80),
    ("2", "gate", "readiness", 200, 80),
    ("3", "artifact", "readiness.md", 320, 80),
    ("4", "handover", "", 420, 80),
    ("5", "stage", "PRESALES", 520, 80),
    ("6", "gate", "handover", 640, 80),
    ("7", "artifact", "handover.md", 760, 80),
    ("8", "handover", "", 860, 80),
    ("9", "stage", "ARCHITECTURE", 960, 80),
    ("10", "gate", "solution_baseline", 1100, 80),
    ("11", "artifact", "solution-baseline.md", 1220, 80),
    ("12", "handover", "", 1320, 80),
    ("13", "stage", "DELIVERY", 1420, 80),
    ("14", "gate", "acceptance", 1540, 80),
    ("15", "artifact", "handover.md", 1660, 80),
]


def build_lifecycle_diagram() -> str:
    """Build draw.io XML for the EPE lifecycle flow."""
    root = ET.Element("mxGraphModel", {"grid": "1", "gridSize": "10", "guides": "1", "tooltips": "1", "connect": "1", "fold": "1", "page": "1", "pageScale": "1", "pageWidth": "1800", "pageHeight": "200"})

    root_cell = ET.SubElement(root, "root")
    ET.SubElement(root_cell, "mxCell", {"id": "0"})
    ET.SubElement(root_cell, "mxCell", {"id": "1", "parent": "0"})

    # Add stage boxes
    for id_, type_, label, x, y in LIFECYCLE_LAYOUT:
        style = LIFECYCLE_STYLES.get(type_, "")
        if type_ == "handover":
            # Arrow from previous to next
            prev = str(int(id_) - 1)
            ET.SubElement(root_cell, "mxCell", {
                "id": f"e{prev}",
                "edge": "1",
                "parent": "1",
                "source": prev,
                "target": id_,
                "style": LIFECYCLE_STYLES["handover"],
            })
        else:
            ET.SubElement(root_cell, "mxCell", {
                "id": id_,
                "parent": "1",
                "value": label,
                "style": style,
                "x": str(x),
                "y": str(y),
                "width": "100",
                "height": "40",
            })

    return ET.tostring(root, encoding="unicode")


# ---------------------------------------------------------------------------
# Traceability Spine diagram
# ---------------------------------------------------------------------------

TRACEABILITY_LAYOUT = [
    # (id, label, style_key, x, y, width, height)
    ("C1", "CUST", "entity", 50, 200, 80, 40),
    ("R1", "REQ", "entity", 250, 200, 80, 40),
    ("C2", "COMP", "entity", 450, 200, 80, 40),
    ("D1", "DEC", "entity", 650, 200, 80, 40),
    ("T1", "TEST", "entity", 850, 200, 80, 40),
    ("E1", "EVD", "entity", 1050, 200, 80, 40),
    ("AC1", "ACCEPTANCE", "entity", 1250, 200, 100, 40),
    ("AB1", "AS-BUILT", "entity", 1450, 200, 100, 40),
]

TRACEABILITY_STYLES = {
    "entity": "rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontStyle=1;fontSize=12",
    "edge": "endArrow=block;html=1;strokeWidth=1;strokeColor=#666666;dashed=0",
    "cross": "endArrow=block;html=1;strokeWidth=1;strokeColor=#d6b656;dashed=1",
}


def build_traceability_diagram() -> str:
    """Build draw.io XML for the unified traceability spine."""
    root = ET.Element("mxGraphModel", {"grid": "1", "gridSize": "10", "guides": "1", "tooltips": "1", "connect": "1", "fold": "1", "page": "1", "pageScale": "1", "pageWidth": "1600", "pageHeight": "350"})

    root_cell = ET.SubElement(root, "root")
    ET.SubElement(root_cell, "mxCell", {"id": "0"})
    ET.SubElement(root_cell, "mxCell", {"id": "1", "parent": "0"})

    # Title
    ET.SubElement(root_cell, "mxCell", {
        "id": "title",
        "parent": "1",
        "value": "EPE Traceability Spine — Unified ID Graph",
        "style": "text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=16;fontStyle=1",
        "x": "50",
        "y": "30",
        "width": "600",
        "height": "30",
    })

    # Spine entities
    for id_, label, style_key, x, y, w, h in TRACEABILITY_LAYOUT:
        style = TRACEABILITY_STYLES.get(style_key, "")
        ET.SubElement(root_cell, "mxCell", {
            "id": id_,
            "parent": "1",
            "value": label,
            "style": style,
            "x": str(x),
            "y": str(y),
            "width": str(w),
            "height": str(h),
        })

    # Edges between spine entities
    spine_edges = [
        ("C1", "R1", "refines"),
        ("R1", "C2", "satisfied_by"),
        ("C2", "D1", "decided_by"),
        ("D1", "T1", "validated_by"),
        ("T1", "E1", "verified_by"),
        ("E1", "AC1", "accepted_by"),
        ("AC1", "AB1", "produces"),
    ]
    edge_style = "endArrow=block;html=1;strokeWidth=2;strokeColor=#6c8ebf"
    for idx, (src, tgt, label) in enumerate(spine_edges):
        ET.SubElement(root_cell, "mxCell", {
            "id": f"e{idx}",
            "edge": "1",
            "parent": "1",
            "source": src,
            "target": tgt,
            "style": edge_style,
            "value": label,
        })

    # Cross-cutting section
    cross_y = 280
    ET.SubElement(root_cell, "mxCell", {
        "id": "cross_title",
        "parent": "1",
        "value": "Cross-cutting entities:",
        "style": "text;html=1;strokeColor=none;fillColor=none;fontSize=12;fontStyle=1",
        "x": "50",
        "y": str(cross_y),
        "width": "150",
        "height": "20",
    })

    cross_entities = [
        ("ASM", "Assumptions (affects REQ)", 200),
        ("DEP", "Dependencies (blocks REQ)", 450),
        ("CHG", "Change Requests (modifies)", 700),
    ]
    for id_, label, x in cross_entities:
        ET.SubElement(root_cell, "mxCell", {
            "id": id_,
            "parent": "1",
            "value": f"{id_}\n{label}",
            "style": "rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=10",
            "x": str(x),
            "y": str(cross_y + 20),
            "width": "130",
            "height": "40",
        })
        # Arrow from cross entity to REQ
        ET.SubElement(root_cell, "mxCell", {
            "id": f"cross_{id_}",
            "edge": "1",
            "parent": "1",
            "source": id_,
            "target": "R1",
            "style": "endArrow=block;html=1;strokeWidth=1;strokeColor=#d6b656;dashed=1",
        })

    return ET.tostring(root, encoding="unicode")


# ---------------------------------------------------------------------------
# Component Map (Tele-MANAS 15 components)
# ---------------------------------------------------------------------------

TELE_MANAS_COMPONENTS = [
    ("COMP-001", "Citizen Channel", 50, 80),
    ("COMP-002", "Tele-MANAS Core", 200, 80),
    ("COMP-003", "E-Sanjeevani Adapter", 350, 80),
    ("COMP-004", "ABDM Gateway", 500, 80),
    ("COMP-005", "E-Manas EHR", 650, 80),
    ("COMP-006", "Governance Dashboard", 50, 180),
    ("COMP-007", "Training", 200, 180),
    ("COMP-008", "Integration Bus", 350, 180),
    ("COMP-009", "IAM/AAA", 500, 180),
    ("COMP-010", "Observability SRE", 650, 180),
    ("COMP-011", "DevSecOps", 50, 280),
    ("COMP-012", "L1/L2 Support", 200, 280),
    ("COMP-013", "Data Protection", 350, 280),
    ("COMP-014", "State Rollout Orch", 500, 280),
    ("COMP-015", "Commercial IVR", 650, 280),
]


def build_component_map() -> str:
    """Build draw.io XML for Tele-MANAS component map (15 components)."""
    root = ET.Element("mxGraphModel", {"grid": "1", "gridSize": "10", "guides": "1", "tooltips": "1", "connect": "1", "fold": "1", "page": "1", "pageScale": "1", "pageWidth": "800", "pageHeight": "400"})

    root_cell = ET.SubElement(root, "root")
    ET.SubElement(root_cell, "mxCell", {"id": "0"})
    ET.SubElement(root_cell, "mxCell", {"id": "1", "parent": "0"})

    # Title
    ET.SubElement(root_cell, "mxCell", {
        "id": "title",
        "parent": "1",
        "value": "Tele-MANAS Solution Components (COMP-NNN)",
        "style": "text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=14;fontStyle=1",
        "x": "50",
        "y": "20",
        "width": "700",
        "height": "30",
    })

    # Components
    component_style = "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=10"
    for comp_id, name, x, y in TELE_MANAS_COMPONENTS:
        ET.SubElement(root_cell, "mxCell", {
            "id": comp_id,
            "parent": "1",
            "value": f"{comp_id}\n{name}",
            "style": component_style,
            "x": str(x),
            "y": str(y),
            "width": "130",
            "height": "60",
        })

    # Key relationships (edges)
    relationships = [
        ("COMP-001", "COMP-002", "User access"),
        ("COMP-002", "COMP-003", "Video calls"),
        ("COMP-002", "COMP-004", "ABDM sync"),
        ("COMP-002", "COMP-005", "EHR read/write"),
        ("COMP-002", "COMP-008", "Integrations"),
        ("COMP-004", "COMP-005", "Health records"),
        ("COMP-008", "COMP-009", "Auth"),
        ("COMP-009", "COMP-010", "Audit"),
        ("COMP-010", "COMP-011", "CI/CD"),
        ("COMP-011", "COMP-012", "Ops"),
    ]
    edge_style = "endArrow=block;html=1;strokeWidth=1;strokeColor=#666666;dashed=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0"
    for idx, (src, tgt, label) in enumerate(relationships):
        ET.SubElement(root_cell, "mxCell", {
            "id": f"e{idx}",
            "edge": "1",
            "parent": "1",
            "source": src,
            "target": tgt,
            "style": edge_style,
            "value": label,
        })

    return ET.tostring(root, encoding="unicode")


# ---------------------------------------------------------------------------
# Router class
# ---------------------------------------------------------------------------


@dataclass
class DiagramRequest:
    diagram_type: DiagramType
    project_id: str
    output_path: Path | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class DiagramResult:
    success: bool
    server: MCPServer
    output_path: Path | None = None
    xml_content: str | None = None
    error: str | None = None


class DiagramRouter:
    """Routes diagram requests to the appropriate MCP server.

    MCP server configuration in claude.json:
    {
      "mcpServers": {
        "drawio": { "command": "npx", "args": ["-y", "@drawio/mcp"] },
        "azure": { "command": "python", "args": ["-m", "azure_drawio_mcp"] },
        "server": { "command": "node", "args": ["server.js"] }
      }
    }

    MCP Tool invocations:
      - jgraph/drawio-mcp: create_diagram(xml=xml_content, title=name)
      - Azure-DrawIO-MCP: generate_azure_diagram(architecture=content)
      - lgazo/drawio-mcp-server: create_document() → add_shape() → save_document()
    """

    def __init__(self, mcp_servers: dict[str, Any] | None = None) -> None:
        self._servers = mcp_servers or {}

    def route(self, request: DiagramRequest) -> MCPServer:
        """Route a request to the appropriate MCP server."""
        content = request.metadata.get("content", "")
        inline = request.metadata.get("inline", False)
        return route(request.diagram_type, content=content, inline=inline)

    def render(self, request: DiagramRequest) -> DiagramResult:
        """Render a diagram using the appropriate MCP server.

        When MCP servers are configured, this method will:
        1. Route to the correct MCP server
        2. Invoke the appropriate tool (create_diagram, generate_azure_diagram, etc.)
        3. Return the result

        Currently generates XML directly when MCP servers are unavailable.
        """
        # Select the appropriate server
        server = self.route(request)

        # Build the XML content
        xml_content = self._build_xml(request.diagram_type)

        # Write output file
        output_path = request.output_path
        if output_path:
            op = Path(output_path) if isinstance(output_path, str) else output_path
            op.parent.mkdir(parents=True, exist_ok=True)
            op.write_text(xml_content, encoding="utf-8")
            output_path = op

        return DiagramResult(
            success=True,
            server=server,
            output_path=output_path,
            xml_content=xml_content,
        )

    def _build_xml(self, diagram_type: DiagramType) -> str:
        """Build draw.io XML for the given diagram type."""
        builders = {
            DiagramType.LIFECYCLE_FLOW: build_lifecycle_diagram,
            DiagramType.TRACEABILITY_SPINE: build_traceability_diagram,
            DiagramType.COMPONENT_MAP: build_component_map,
        }
        builder = builders.get(diagram_type)
        if builder:
            return builder()
        return build_lifecycle_diagram()  # default
