function buildMetadata(State) {

    // @TODO: Complete the following function that builds the metadata panel
  
    // Use `d3.json` to fetch the metadata for a sample
    var url = `/metadata/${State}`;
    d3.json(url).then(function(State){ 
      // Use d3 to select the panel with id of `#sample-metadata`
      var useyr_891617 = d3.select("#useyr_891617");

      // Use `.html("") to clear any existing metadata
      useyr_891617.html("");


      // Use `Object.entries` to add each key and value pair to the panel
      // Hint: Inside the loop, you will need to use d3 to append new
      // tags for each key-value in the metadata.
      Object.entries(State).forEach(function ([key, value]) {
        var row = useyr_891617.append("p");
        row.text(`${key}: ${value}`);
  
  });
    }
  )};  
      

  
function buildCharts(State) {
  
    // @TODO: Use `d3.json` to fetch the sample data for the plots
    var url = `/arrest_prispop_data/${State}`;
    d3.json(url).then(function(data) {
    
      // @TODO: Build a Bubble Chart using the sample data
      var x_values = data.dt_ids;
      var y_values = data.state_values;
      var m_size = data.state_values;
      var m_colors = data.dt_ids; 
      var t_values = data.dt_information;
      
      var trace1 = {
        x: x_values,
        y: y_values,
        text: t_values,
        mode: 'markers',
        marker: {
          color: m_colors,
          size: m_size
        } 
      };
    
      var data = [trace1];
  
      var layout = {
        xaxis: { title: "DATA ID"},
      };

      Plotly.newPlot('bubble', data, layout);

      // @TODO: Build a Pie Chart
      d3.json(url).then(function(data) {  
        var pie_values = data.state_values.slice(0,10);
          var pie_labels = data.dt_ids.slice(0,10);
          var pie_hover = data.dt_labels.slice(0,10);
    
          var data = [{
            values: pie_values,
            labels: pie_labels,
            hovertext: pie_hover,
            type: 'pie'
          }];
    
          Plotly.newPlot('pie', data);
    
        });
      });   
    }
      
  
  function init() {
    // Grab a reference to the dropdown select element
    var selector = d3.select("#selDataset");
  
    // Use the list of sample names to populate the select options
    d3.json("/names").then((StateNames) => {
        StateNames.forEach((State) => {
        selector
          .append("option")
          .text(State)
          .property("value", State);
      });
  
      // Use the first sample from the list to build the initial plots
      const firstState = StateNames[0];
      buildCharts(firstState);
      buildMetadata(firstState);
    });
  }
  
  function optionChanged(newState) {
    // Fetch new data each time a new sample is selected
    buildCharts(newState);
    buildMetadata(newState);
  }
  
  // Initialize the dashboard
  init();
  