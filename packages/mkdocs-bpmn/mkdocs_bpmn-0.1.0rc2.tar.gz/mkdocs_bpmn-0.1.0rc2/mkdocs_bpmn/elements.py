from lxml.html import Element


def create_style_element():
    style = Element("style")
    style.text = """
         .mk-bpmn-container svg {
            height: 100% !important;
         }

         button.fullscreen-button {
             position: absolute;
             top: 15px;
             right: 15px;
             color: rgb(64, 64, 64);
             background: rgba(0,0,0,0.05);
             border: 0;
             width: 30px;
             height: 30px;
             border-radius: 50%;
             box-sizing: border-box;
             transition: transform .3s;
             cursor: pointer;
             display: flex;
             flex-direction: column;
             justify-content: center;
         }

         button.fullscreen-button:hover {
             transform: scale(1.125);
         }
    """
    return style


def create_bpmn_lib_element(bpmn_lib_url):
    script = Element("script")
    script.attrib["src"] = bpmn_lib_url
    return script


def create_render_script_element():
    script = Element("script")
    script.text = """
        function fetchDiagram(url) {
          return fetch(url).then((response) => response.text());
        }
        
        async function renderDiagram(container) {
          const id = container.getAttribute("id");
          const src = container.getAttribute("src");
          const width = container.getAttribute("width") || "100%";
          const height = container.getAttribute("height") || "100%";
          const zoom = container.getAttribute("zoom") || "fit-viewport";
          const fullscreen = container.getAttribute("fullscreen") == "true";
        
          const bpmnViewer = new BpmnJS({
            container: "#" + id,
            width: width,
            height: height,
          });
          const diagram = await fetchDiagram(src);
          await bpmnViewer.importXML(diagram);
          const canvas = bpmnViewer.get("canvas");
          canvas.zoom(zoom);
        
          if (fullscreen) {
            const button = document.createElement("button");
            button.innerHTML = `
                    <svg viewBox="0 0 24 24">
                        <path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 
                        7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/>
                    </svg>
                    `;
            button.classList.add("fullscreen-button");
            canvas.getContainer().parentElement.appendChild(button);
            button.addEventListener("click", () => {
              canvas.getContainer().requestFullscreen();
            });
          }
        }
        
        document.querySelectorAll(".mk-bpmn-container").forEach((c) => {
          renderDiagram(c);
        });
    """
    return script
