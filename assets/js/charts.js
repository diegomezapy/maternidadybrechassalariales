export function initCharts(data) {
    if (typeof echarts === 'undefined') {
        console.error("ECharts no cargó correctamente.");
        return;
    }

    const brechasChart = echarts.init(document.getElementById('chart-brechas'));
    const edadesChart = echarts.init(document.getElementById('chart-edades'));
    
    // Resize listeners
    window.addEventListener('resize', () => {
        brechasChart.resize();
        edadesChart.resize();
    });

    const selector = document.getElementById('dim-selector');
    
    function renderBrechasTable(dimension) {
        const items = data.brechas[dimension];
        const tbody = items.map((item, i) => `
            <tr class="${i % 2 === 0 ? 'bg-gray-50' : 'bg-white'} border-b">
                <td class="py-3 px-4 font-medium text-gray-700">${item.categoria}</td>
                <td class="py-3 px-4 text-right text-primary font-bold">${item.tasa.toFixed(1)}%</td>
                <td class="py-3 px-4 text-right text-gray-500 text-xs">${item.poblacion.toLocaleString('es-PY')}</td>
            </tr>
        `).join('');

        document.getElementById('table-brechas').innerHTML = `
            <table class="min-w-full text-left border-collapse">
                <thead>
                    <tr class="border-b bg-gray-100">
                        <th class="py-2 px-4 font-semibold text-gray-600">Categoría</th>
                        <th class="py-2 px-4 text-right font-semibold text-gray-600">Tasa Uso</th>
                        <th class="py-2 px-4 text-right font-semibold text-gray-600">Población Base</th>
                    </tr>
                </thead>
                <tbody>${tbody}</tbody>
            </table>
        `;
    }

    function updateBrechasChart(dimension) {
        const dimensionData = data.brechas[dimension];
        const labels = dimensionData.map(d => d.categoria);
        const values = dimensionData.map(d => d.tasa);

        const option = {
            title: {
                text: 'Tasa de Uso de Internet (%)',
                left: 'center',
                textStyle: {
                    color: '#334155',
                    fontSize: 16,
                    fontWeight: 'normal'
                }
            },
            tooltip: {
                trigger: 'axis',
                formatter: '{b}: {c}%',
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                borderColor: '#e2e8f0',
                textStyle: { color: '#0f172a' }
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '10%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: labels,
                axisLabel: {
                    interval: 0,
                    rotate: labels.length > 5 ? 30 : 0
                }
            },
            yAxis: {
                type: 'value',
                max: 100,
                axisLabel: { formatter: '{value}%' }
            },
            series: [
                {
                    data: values,
                    type: 'bar',
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: '#C78B58' },
                            { offset: 1, color: '#5E412F' }
                        ]),
                        borderRadius: [4, 4, 0, 0]
                    },
                    label: {
                        show: true,
                        position: 'top',
                        formatter: '{c}%',
                        color: '#64748b'
                    }
                }
            ]
        };

        brechasChart.setOption(option);
        renderBrechasTable(dimension);
    }

    // Inicializar Brechas
    updateBrechasChart(selector.value);
    
    // Listener Selector
    selector.addEventListener('change', (e) => {
        updateBrechasChart(e.target.value);
    });

    // Gráfico de Edades
    const datosEdades = data.brechas.grupo_edad;
    const edadesOption = {
        tooltip: {
            trigger: 'axis',
            formatter: '{b}: {c}%'
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '5%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
            max: 100,
            axisLabel: { formatter: '{value}%' }
        },
        yAxis: {
            type: 'category',
            data: datosEdades.map(d => d.categoria).reverse() // Más jóvenes arriba
        },
        series: [
            {
                type: 'bar',
                data: datosEdades.map(d => d.tasa).reverse(),
                label: {
                    show: true,
                    position: 'right',
                    formatter: '{c}%'
                },
                itemStyle: {
                    color: '#8B5A2B',
                    borderRadius: [0, 4, 4, 0]
                }
            }
        ]
    };
    edadesChart.setOption(edadesOption);
}
