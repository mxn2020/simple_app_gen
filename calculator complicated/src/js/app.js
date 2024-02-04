// Calculator Functions

// Implement basic arithmetic operations
function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

function multiply(a, b) {
  return a * b;
}

function divide(a, b) {
  if (b !== 0) {
    return a / b;
  } else {
    return 'Error: Division by zero';
  }
}

// Implement advanced operations
function exponentiation(base, exponent) {
  return Math.pow(base, exponent);
}

function squareRoot(number) {
  return Math.sqrt(number);
}

// Memory functions
let memory = 0;

function storeInMemory(value) {
  memory = value;
}

function recallFromMemory() {
  return memory;
}

// History tracking
let history = [];

function addToHistory(operation) {
  history.push(operation);
}

// Event handling
// Add event listeners to calculator buttons to trigger corresponding functions