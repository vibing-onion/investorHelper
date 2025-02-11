const loadIndexChart = () => {
    fetch('http://127.0.0.1:5000/sample_data')
        .then(res => res.json())
        .then(d => {
            console.log(d)
            spx = []
            nasdaq = []
            d.forEach(e => {
                spx.push({
                    x: new Date(e[e.length-1]),
                    y: e[0]
                })
                nasdaq.push({
                    x: new Date(e[e.length-1]),
                    y: e[1]
                })
            });

            const ctx = new CanvasJS.Chart('indexChart', {
                animationEnabled: true,
                data: [{
                    indexLabelFontColor: "darkSlateGray",
                    type: "area",
                    yValueFormatString: "####.##%",
                    dataPoints: spx
                },
                {
                    indexLabelFontColor: "darkSlateGray",
                    type: "area",
                    yValueFormatString: "####.##%",
                    dataPoints: nasdaq
                }
            ]
            });

            ctx.render()
            console.log('done')
})}

loadIndexChart()