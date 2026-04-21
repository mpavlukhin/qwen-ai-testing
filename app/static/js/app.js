/**
 * Calculator Hub - Frontend JavaScript
 * Handles all calculator operations and UI interactions
 */

// ==================== Tab Navigation ====================

document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons and contents
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked button and corresponding content
        btn.classList.add('active');
        const tabId = btn.dataset.tab;
        document.getElementById(tabId).classList.add('active');
        
        // Load history if history tab is selected
        if (tabId === 'history') {
            loadHistory();
        }
    });
});

// ==================== Utility Functions ====================

function showResult(elementId, data, isError = false) {
    const element = document.getElementById(elementId);
    element.className = 'result-box show' + (isError ? ' error' : '');
    
    let html = `<h4>${isError ? 'Error' : 'Result'}</h4>`;
    
    if (typeof data === 'object') {
        html += '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
    } else {
        html += `<p>${data}</p>`;
    }
    
    element.innerHTML = html;
}

async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    
    const response = await fetch(endpoint, options);
    const result = await response.json();
    
    if (!response.ok) {
        throw new Error(result.detail || 'An error occurred');
    }
    
    return result;
}

// ==================== Math Calculator ====================

async function calculateMath() {
    try {
        const a = parseFloat(document.getElementById('math-a').value);
        const b = parseFloat(document.getElementById('math-b').value);
        const operation = document.getElementById('math-operation').value;
        
        if (isNaN(a) || (operation !== 'sqrt' && isNaN(b))) {
            throw new Error('Please enter valid numbers');
        }
        
        const payload = { operation, a, b };
        if (operation === 'power') {
            payload.base = a;
            payload.exponent = b;
        }
        
        const result = await apiRequest('/api/math/calculate', 'POST', payload);
        showResult('math-result', { operation: result.operation, result: result.result });
    } catch (error) {
        showResult('math-result', error.message, true);
    }
}

async function calculateAdvanced() {
    try {
        const operation = document.getElementById('adv-operation').value;
        const value = parseFloat(document.getElementById('adv-value').value);
        const degrees = document.getElementById('degrees-checkbox').checked;
        
        if (isNaN(value)) {
            throw new Error('Please enter a valid number');
        }
        
        const payload = { operation, value, degrees };
        if (operation === 'factorial') {
            payload.n = Math.floor(value);
        }
        
        const result = await apiRequest('/api/math/calculate', 'POST', payload);
        showResult('adv-result', { operation: result.operation, result: result.result });
    } catch (error) {
        showResult('adv-result', error.message, true);
    }
}

// ==================== Finance Calculator ====================

async function calculateDiscount() {
    try {
        const price = parseFloat(document.getElementById('discount-price').value);
        const discountPercent = parseFloat(document.getElementById('discount-percent').value);
        
        if (isNaN(price) || isNaN(discountPercent)) {
            throw new Error('Please enter valid numbers');
        }
        
        const result = await apiRequest('/api/finance/discount', 'POST', { price, discount_percent: discountPercent });
        delete result.success;
        showResult('discount-result', result);
    } catch (error) {
        showResult('discount-result', error.message, true);
    }
}

async function calculateLoan() {
    try {
        const principal = parseFloat(document.getElementById('loan-principal').value);
        const annualRate = parseFloat(document.getElementById('loan-rate').value);
        const years = parseInt(document.getElementById('loan-years').value);
        
        if (isNaN(principal) || isNaN(annualRate) || isNaN(years)) {
            throw new Error('Please enter valid numbers');
        }
        
        const result = await apiRequest('/api/finance/loan', 'POST', { principal, annual_rate: annualRate, years });
        delete result.success;
        showResult('loan-result', result);
    } catch (error) {
        showResult('loan-result', error.message, true);
    }
}

async function calculateROI() {
    try {
        const investment = parseFloat(document.getElementById('roi-investment').value);
        const returnValue = parseFloat(document.getElementById('roi-return').value);
        
        if (isNaN(investment) || isNaN(returnValue)) {
            throw new Error('Please enter valid numbers');
        }
        
        const result = await apiRequest('/api/finance/roi', 'POST', { investment, return_value: returnValue });
        delete result.success;
        showResult('roi-result', result);
    } catch (error) {
        showResult('roi-result', error.message, true);
    }
}

async function calculateVAT() {
    try {
        const amount = parseFloat(document.getElementById('vat-amount').value);
        const vatRate = parseFloat(document.getElementById('vat-rate').value);
        const inclusive = document.getElementById('vat-inclusive').checked;
        
        if (isNaN(amount) || isNaN(vatRate)) {
            throw new Error('Please enter valid numbers');
        }
        
        const result = await apiRequest('/api/finance/vat', 'POST', { amount, vat_rate: vatRate, inclusive });
        delete result.success;
        showResult('vat-result', result);
    } catch (error) {
        showResult('vat-result', error.message, true);
    }
}

async function calculateCompoundInterest() {
    try {
        const principal = parseFloat(document.getElementById('ci-principal').value);
        const annualRate = parseFloat(document.getElementById('ci-rate').value);
        const years = parseInt(document.getElementById('ci-years').value);
        const compoundsPerYear = parseInt(document.getElementById('ci-compounds').value);
        
        if (isNaN(principal) || isNaN(annualRate) || isNaN(years)) {
            throw new Error('Please enter valid numbers');
        }
        
        const result = await apiRequest('/api/finance/compound-interest', 'POST', {
            principal,
            annual_rate: annualRate,
            years,
            compounds_per_year: compoundsPerYear
        });
        delete result.success;
        showResult('ci-result', result);
    } catch (error) {
        showResult('ci-result', error.message, true);
    }
}

// ==================== Health Calculator ====================

async function calculateBMI() {
    try {
        const weightKg = parseFloat(document.getElementById('bmi-weight').value);
        const heightCm = parseFloat(document.getElementById('bmi-height').value);
        
        if (isNaN(weightKg) || isNaN(heightCm)) {
            throw new Error('Please enter valid numbers');
        }
        
        const result = await apiRequest('/api/health/bmi', 'POST', { weight_kg: weightKg, height_cm: heightCm });
        delete result.success;
        showResult('bmi-result', result);
    } catch (error) {
        showResult('bmi-result', error.message, true);
    }
}

async function calculateBMR() {
    try {
        const weightKg = parseFloat(document.getElementById('bmr-weight').value);
        const heightCm = parseFloat(document.getElementById('bmr-height').value);
        const age = parseInt(document.getElementById('bmr-age').value);
        const gender = document.getElementById('bmr-gender').value;
        
        if (isNaN(weightKg) || isNaN(heightCm) || isNaN(age)) {
            throw new Error('Please enter valid numbers');
        }
        
        const result = await apiRequest('/api/health/bmr', 'POST', { weight_kg: weightKg, height_cm: heightCm, age, gender });
        delete result.success;
        showResult('bmr-result', result);
    } catch (error) {
        showResult('bmr-result', error.message, true);
    }
}

async function calculateWaterIntake() {
    try {
        const weightKg = parseFloat(document.getElementById('water-weight').value);
        const activityMinutes = parseInt(document.getElementById('water-activity').value) || 0;
        const climate = document.getElementById('water-climate').value;
        
        if (isNaN(weightKg)) {
            throw new Error('Please enter valid weight');
        }
        
        const result = await apiRequest('/api/health/water-intake', 'POST', {
            weight_kg: weightKg,
            activity_minutes: activityMinutes,
            climate
        });
        delete result.success;
        showResult('water-result', result);
    } catch (error) {
        showResult('water-result', error.message, true);
    }
}

async function calculateTDEE() {
    try {
        const weightKg = parseFloat(document.getElementById('tdee-weight').value);
        const heightCm = parseFloat(document.getElementById('tdee-height').value);
        const age = parseInt(document.getElementById('tdee-age').value);
        const gender = document.getElementById('tdee-gender').value;
        const activityLevel = document.getElementById('tdee-activity').value;
        
        if (isNaN(weightKg) || isNaN(heightCm) || isNaN(age)) {
            throw new Error('Please enter valid numbers');
        }
        
        const result = await apiRequest('/api/health/tdee', 'POST', {
            weight_kg: weightKg,
            height_cm: heightCm,
            age,
            gender,
            activity_level: activityLevel
        });
        delete result.success;
        showResult('tdee-result', result);
    } catch (error) {
        showResult('tdee-result', error.message, true);
    }
}

// ==================== Unit Converter ====================

let unitOptions = {};

async function updateUnitOptions() {
    const category = document.getElementById('conv-category').value;
    
    try {
        const result = await apiRequest(`/api/converter/units/${category}`);
        unitOptions[category] = result.units;
        
        const fromSelect = document.getElementById('conv-from');
        const toSelect = document.getElementById('conv-to');
        
        fromSelect.innerHTML = '';
        toSelect.innerHTML = '';
        
        result.units.forEach(unit => {
            fromSelect.add(new Option(unit, unit));
            toSelect.add(new Option(unit, unit));
        });
        
        // Set different default values
        if (result.units.length > 1) {
            toSelect.selectedIndex = 1;
        }
    } catch (error) {
        console.error('Error loading units:', error);
    }
}

async function convertUnits() {
    try {
        const value = parseFloat(document.getElementById('conv-value').value);
        const category = document.getElementById('conv-category').value;
        const fromUnit = document.getElementById('conv-from').value;
        const toUnit = document.getElementById('conv-to').value;
        
        if (isNaN(value)) {
            throw new Error('Please enter a valid number');
        }
        
        const result = await apiRequest('/api/converter/convert', 'POST', {
            value,
            category,
            from_unit: fromUnit,
            to_unit: toUnit
        });
        
        delete result.success;
        showResult('conv-result', {
            conversion: `${result.input_value} ${result.input_unit} = ${result.output_value} ${result.output_unit}`,
            details: result
        });
    } catch (error) {
        showResult('conv-result', error.message, true);
    }
}

// Initialize converter on page load
updateUnitOptions();

// ==================== History ====================

async function loadHistory() {
    try {
        const result = await apiRequest('/api/history');
        const historyList = document.getElementById('history-list');
        
        if (!result.data || result.data.length === 0) {
            historyList.innerHTML = '<p class="empty-state">No calculations yet. Start calculating!</p>';
            return;
        }
        
        historyList.innerHTML = result.data.map(item => `
            <div class="history-item">
                <div class="history-item-header">
                    <span class="history-type">${item.calculator_type}</span>
                    <span class="history-time">${new Date(item.created_at).toLocaleString()}</span>
                </div>
                <div class="history-details">
                    <strong>Operation:</strong> ${item.operation}<br>
                    <strong>Input:</strong> ${JSON.stringify(item.input_data)}<br>
                    <strong>Result:</strong> ${JSON.stringify(item.result_data)}
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

async function clearHistory() {
    if (!confirm('Are you sure you want to clear all calculation history?')) {
        return;
    }
    
    try {
        const result = await apiRequest('/api/history', 'DELETE');
        alert(result.message);
        loadHistory();
    } catch (error) {
        alert('Error clearing history: ' + error.message);
    }
}

// ==================== Keyboard Support ====================

// Allow Enter key to trigger calculations
document.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && e.target.tagName === 'INPUT') {
        const activeTab = document.querySelector('.tab-content.active');
        const button = activeTab.querySelector('.btn-primary');
        if (button) {
            button.click();
        }
    }
});
