<script lang="ts">
    import { onMount } from 'svelte';
    import cytoscape from 'cytoscape';

    let { edges, nodes, edgeLabels, selectedNode } = $props();

    let height: string = '70vh';
    let width: string = '100%';
  
    let container: HTMLElement;
    let cy: any;
    let graphData: { nodes: any[], edges: any[] } = { nodes: [], edges: [] };

    let visibleLabels = new Set(edgeLabels);

    if(edgeLabels.indexOf('subclass of') > -1 && edgeLabels.indexOf('superclass of') > -1){
      visibleLabels.clear;
      visibleLabels.add('subclass of');
      visibleLabels.add('superclass of');
    };
  

    onMount(() => {
      initializeGraph();
    });

    function initializeGraph() {

      graphData = {nodes, edges};

      if (!container || graphData.nodes.length === 0) return;
  
      const elements = [
        ...graphData.nodes.map(node => ({
          data: {
            id: node.id,
            label: node.label,
            entityType: 'class'
          }
        })),
        
        ...graphData.edges.map(edge => ({
          data: {
            id: edge.id,
            source: edge.sourceId,
            target: edge.targetId,
            label: edge.label,
            entityType: 'property'
          }
        }))
      ];

      cy = cytoscape({
        container,
        elements,
        style: [
          {
            selector: 'node',
            style: {
              'background-color': '#182E48',
              'label': 'data(label)',
              'color': '#FEF9E1',
              'text-valign': 'center',
              'text-halign': 'center',
              'text-wrap': 'wrap',
              'text-max-width': '100px',
              'width': '100px',
              'height': '40px',
              'padding': '10px',
              'font-size': '12px',
              'shape': 'round-rectangle'
            }
          },
          {
            selector: 'node.highlighted',
            style: {
              'border-opacity': 1,
              'border-color': '#A12332',
              'border-width': 3,
              'background-color': '#D62839'
            }
          },
          {
            selector: 'edge',
            style: {
              'width': 2,
              'line-color': '#DE7C73',
              'target-arrow-color': '#DE7C73',
              'target-arrow-shape': 'triangle',
              'curve-style': 'straight',
              'label': 'data(label)',
              'font-size': '10px',
              'text-rotation': 'none',
              'text-background-color': 'white',
              'text-background-opacity': 0.8,
              'text-background-padding': '2px'
            }
          }
        ],
        layout: {
          // name: 'concentric'
          // name: 'breadthfirst'
          // name: 'circle'
          // name: 'grid'
          name: 'cose',
          animate: false,
          nodeOverlap: 20,
          idealEdgeLength: () => 100,
          nodeRepulsion: () => 400000,
          edgeElasticity: () => 100,
          nestingFactor: 5,
          gravity: 80,
          numIter: 1000,
          fit: true,
          padding: 30
        }
      });
  
      cy.on('tap', 'node', function(evt: cytoscape.EventObject) {
        const node = evt.target;
        console.log('Node clicked:', node.data());
      });
  
      cy.on('tap', 'edge', function(evt: cytoscape.EventObject) {
        const edge = evt.target;
        console.log('Edge clicked:', edge.data());
      });
  
      cy.userZoomingEnabled(true);
      cy.userPanningEnabled(true);

      updateEdgeVisibility();
    }

    $effect (() => {
      if ( !cy || !selectedNode) return;

      cy.nodes().removeClass('highlighted');
      const node = cy.getElementById(selectedNode);
      if (node && node.length > 0) {
        node.addClass('highlighted');
        cy.center(node);
        cy.zoom({ level: 1.5, position: node.position() });
      }
    });

    
    function toggleLabel(label: string) {
      if (visibleLabels.has(label)) {
        visibleLabels.delete(label);
      } else {
        visibleLabels.add(label);
      }
      updateEdgeVisibility();
    }

    function updateEdgeVisibility() {
      if (!cy) return;

      cy.edges().forEach((edge: { data: (arg0: string) => any; style: (arg0: string, arg1: string) => void; }) => {
        const label = edge.data('label');
        edge.style('display', visibleLabels.has(label) ? 'element' : 'none');
      });
    }

    function recenter(){
      if (cy) {
        cy.fit(undefined, 40);
        cy.zoom({lever : 1});
        cy.nodes().removeClass('highlighted');
      }
    }

  </script>


  <div class="border-2 rounded overflow-hidden relative border-solid border-darker-light dark:border-lighter-dark" bind:this={container} style="height: {height}; width: {width};">
    <div class="absolute z-10"> 
      <div class="mt-2 ml-2 p-2 border border-solid border-accent-dark bg-darker-light dark:bg-lighter-dark w-50">
        {#each edgeLabels as label}
          <label class="text-lighter-dark dark:text-darker-light ">
            <input type="checkbox" checked={visibleLabels.has(label)} onchange={() => toggleLabel(label)}/>
            {label}
          </label><br />
        {/each}
      </div>
      <button class="ml-2 p-2 border border-solid border-accent-dark text-darker-light dark:text-darker-dark bg-lighter-dark dark:bg-darker-light hover:font-semibold w-50" onclick={recenter}>Zresetuj wizualizację</button>
    </div>
  </div>
  

