<script lang="ts">
    import { onMount } from 'svelte';
    import cytoscape from 'cytoscape';

    let { edges, nodes } = $props();

    let height: string = '70vh';
    let width: string = '100%';
  
    let container: HTMLElement;
    let cy: any;
    let isLoading: boolean = false;
    let error: string | null = null;
    let graphData: { nodes: any[], edges: any[] } = { nodes: [], edges: [] };
  
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
              'width': '80px',
              'height': '40px',
              'padding': '10px',
              'font-size': '12px',
              'shape': 'round-rectangle'
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
    }
  </script>
  
  <div class="graph-container" bind:this={container} style="height: {height}; width: {width};">
    {#if isLoading}
      <div class="loading-overlay">
        <p>Loading data model...</p>
      </div>
    {:else if error}
      <div class="error-overlay">
        <p>Error: {error}</p>
      </div>
    {/if}
  </div>
  
  <style>
    .graph-container {
      border: 1px solid #ddd;
      border-radius: 4px;
      overflow: hidden;
      position: relative;
    }
    
    .loading-overlay, .error-overlay {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      background-color: rgba(255, 255, 255, 0.8);
      z-index: 10;
    }
    
    .error-overlay {
      background-color: rgba(255, 235, 235, 0.8);
    }

  </style>

