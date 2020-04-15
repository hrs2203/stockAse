// var genLine = () => $.ajax({
//     type: "get",
//     url: '/sample/test_data',
//     success: (response) => {
//         // console.log(response)
//         var ctx = document.getElementById('myChart').getContext('2d');
//         var myChart = new Chart(ctx, {
//             type: 'line',
//             data: {
//                 labels: response.x_axis,
//                 datasets: [
//                     {
//                         label: 'opening -> ',
//                         data: response.y_axis ,
//                         backgroundColor: 'rgba(0,0,0,0)',
//                         borderColor: 'rgba(0,125,255,1)',
//                         borderWidth: 1
//                     },
//                     {
//                         label: 'high -> ',
//                         data: response.y2_axis ,
//                         backgroundColor: 'rgba(0,0,0,0)',
//                         borderColor: 'rgba(0,0,255,1)',
//                         borderWidth: 1
//                     },
//                     {
//                         label: 'low -> ',
//                         data: response.y3_axis ,
//                         backgroundColor: 'rgba(0,0,0,0)',
//                         borderColor: 'rgba(250,0,0,1)',
//                         borderWidth: 1
//                     }
//                 ]
//             },
//             options: {
//                 scales: {
//                     yAxes: [{
//                         ticks: {
//                             min: (Math.min(...response.y3_axis)),
//                             max: Math.floor(Math.max(...response.y_axis)+1)
//                         }
//                     }]
//                 }
//             }
//         });
//     }
// })

// var genLine2 = () => $.ajax({
//     type: "get",
//     url: '/sample/test_data',
//     success: (response) => {
//         // console.log(response)
//         var ctx = document.getElementById('myChart2').getContext('2d');
//         var myChart = new Chart(ctx, {
//             type: 'line',
//             data: {
//                 labels: response.x_axis,
//                 datasets: [
//                     {
//                         label: 'opening -> ',
//                         data: response.y_axis ,
//                         backgroundColor: 'rgba(0,0,0,0)',
//                         borderColor: 'rgba(0,125,255,1)',
//                         borderWidth: 1
//                     },
//                     {
//                         label: 'high -> ',
//                         data: response.y2_axis ,
//                         backgroundColor: 'rgba(0,0,0,0)',
//                         borderColor: 'rgba(0,0,255,1)',
//                         borderWidth: 1
//                     },
//                     {
//                         label: 'low -> ',
//                         data: response.y3_axis ,
//                         backgroundColor: 'rgba(0,0,0,0)',
//                         borderColor: 'rgba(250,0,0,1)',
//                         borderWidth: 1
//                     }
//                 ]
//             },
//             options: {
//                 scales: {
//                     yAxes: [{
//                         ticks: {
//                             min: (Math.min(...response.y3_axis)),
//                             max: Math.floor(Math.max(...response.y_axis)+1)
//                         }
//                     }]
//                 }
//             }
//         });
//     }
// })

var genCompData = (compCode,compKey, chartId) => $.ajax({
    type: "get",
    url: `/company/data/${compCode}/${compKey}`,
    success: (response) => {
        // console.log(response)
        var ctx = document.getElementById(chartId).getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: response.x_axis,
                datasets: [
                    {
                        label: 'opening -> ',
                        data: response.y_axis ,
                        backgroundColor: 'rgba(0,0,0,0)',
                        borderColor: 'rgba(0,125,255,1)',
                        borderWidth: 1,
                        pointRadius: 1
                    },
                    {
                        label: 'high -> ',
                        data: response.y2_axis ,
                        backgroundColor: 'rgba(0,0,0,0)',
                        borderColor: 'rgba(0,0,255,1)',
                        borderWidth: 1,
                        pointRadius: 1
                    },
                    {
                        label: 'low -> ',
                        data: response.y3_axis ,
                        backgroundColor: 'rgba(0,0,0,0)',
                        borderColor: 'rgba(250,0,0,1)',
                        borderWidth: 1,
                        pointRadius: 1
                    }
                ]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            min: (Math.min(...response.y3_axis)),
                            max: Math.floor(Math.max(...response.y2_axis)+1)
                        }
                    }],
                    xAxes: [{
                        gridLines: {
                            color: "rgba(0, 0, 0, 0)",
                        }
                    }]
                }
            }
        });
    }
})


// initial load values
// genLine()
// genLine2()
