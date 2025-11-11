<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Juice Shop</title>
<style>
  body {
    font-family: Arial, sans-serif;
    margin: 20px;
    background: #fafafa;
  }
  h1, h2 {
    color: #2a7a2a;
  }
  .product-list, .order-history {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
  }
  .product, .juice {
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 10px;
    width: 180px;
    text-align: center;
  }
  .product img, .juice img {
    max-width: 100%;
    border-radius: 6px;
  }
  .sizes button {
    margin: 5px 3px;
    padding: 5px 10px;
    border: none;
    background: #4caf50;
    color: white;
    cursor: pointer;
    border-radius: 4px;
  }
  .sizes button:hover {
    background: #45a049;
  }
  #orders {
    margin-top: 30px;
  }
  .order-item {
    background: white;
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #ccc;
  }
</style>
</head>
<body>

<h1>Juice Shop</h1>

<h2>Fruits</h2>
<div class="product-list" id="fruit-list">
  <div class="product"><img src="https://i.imgur.com/1bX5QH6.jpg" alt="Banana" /><p>Banana</p></div>
  <div class="product"><img src="https://i.imgur.com/4zQ9wQD.jpg" alt="Guava" /><p>Guava</p></div>
  <div class="product"><img src="https://i.imgur.com/BW9FzM2.jpg" alt="Apple" /><p>Apple</p></div>
  <div class="product"><img src="https://i.imgur.com/3JsI6uV.jpg" alt="Berries" /><p>Berries</p></div>
  <div class="product"><img src="https://i.imgur.com/K4MdCTD.jpg" alt="Fruit Salad" /><p>Fruit Salad</p></div>
</div>

<h2>Juices & More</h2>
<div class="product-list" id="juice-list">
  <!-- Juices will be inserted here by JS -->
</div>

<h2>Your Order History</h2>
<div id="orders" class="order-history">
  <p>No orders yet</p>
</div>

<script>
const juices = [
  {name: "Guava Juice", img: "https://i.imgur.com/4zQ9wQD.jpg"},
  {name: "Banana Juice", img: "https://i.imgur.com/1bX5QH6.jpg"},
  {name: "Apple Juice", img: "https://i.imgur.com/BW9FzM2.jpg"},
  {name: "Protein Shake", img: "https://i.imgur.com/8pQwX8e.jpg"},
  {name: "Protein Sandwich", img: "https://i.imgur.com/vfK9RG8.jpg"},
];
const prices = { Small: 50, Medium: 60, Large: 70 };

const juiceList = document.getElementById('juice-list');
const ordersDiv = document.getElementById('orders');

// Render juice menu with size buttons
function renderJuices() {
  juices.forEach(juice => {
    const juiceDiv = document.createElement('div');
    juiceDiv.className = 'juice';
    juiceDiv.innerHTML = `
      <img src="${juice.img}" alt="${juice.name}" />
      <p>${juice.name}</p>
      <div class="sizes">
        <button onclick="addOrder('${juice.name}', 'Small')">Small (₹${prices.Small})</button>
        <button onclick="addOrder('${juice.name}', 'Medium')">Medium (₹${prices.Medium})</button>
        <button onclick="addOrder('${juice.name}', 'Large')">Large (₹${prices.Large})</button>
      </div>
    `;
    juiceList.appendChild(juiceDiv);
  });
}

// Add order to localStorage
function addOrder(item, size) {
  const price = prices[size];
  const order = { item, size, price, date: new Date().toLocaleString() };
  let orders = JSON.parse(localStorage.getItem('juiceOrders')) || [];
  orders.push(order);
  localStorage.setItem('juiceOrders', JSON.stringify(orders));
  renderOrders();
  alert(`Added ${item} (${size}) - ₹${price} to your order history.`);
}

// Render order history from localStorage
function renderOrders() {
  let orders = JSON.parse(localStorage.getItem('juiceOrders')) || [];
  if (orders.length === 0) {
    ordersDiv.innerHTML = '<p>No orders yet</p>';
    return;
  }
  ordersDiv.innerHTML = '';
  orders.forEach(order => {
    const div = document.createElement('div');
    div.className = 'order-item';
    div.textContent = `${order.date}: ${order.item} (${order.size}) - ₹${order.price}`;
    ordersDiv.appendChild(div);
  });
}

// Initialize UI
renderJuices();
renderOrders();

</script>

</body>
</html>
