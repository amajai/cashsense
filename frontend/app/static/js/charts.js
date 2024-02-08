const ctx = document.getElementById('myChart');
const dnut = document.getElementById('donutChart');

		  
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
      label: '# of Votes',
      data: [12, 19, 3, 5, 2, 3],
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});

new Chart(dnut, {
  type: 'pie',
  data: {
    labels: [
      'Expense',
      'Income',
    ],
    datasets: [{
      label: 'Finance Data',
      data: [300, 50],
      backgroundColor: [
        'rgb(209, 0, 44)',
        'rgb(54, 162, 235)',
      ],
      hoverOffset: 4
    }]
  }
});
