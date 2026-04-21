#!/usr/bin/env python3
"""
FastAPI Calculator Web Application
A beautiful web app with multiple calculators, tabs, and animations.
Run with: python run.py
"""

import asyncio
import aiosqlite
from datetime import datetime
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import math

# ============================================================================
# CONFIGURATION
# ============================================================================

DB_PATH = "calculators.db"
HOST = "127.0.0.1"
PORT = 8000

# ============================================================================
# DATABASE SETUP
# ============================================================================

async def init_db():
    """Initialize the SQLite database with required tables."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS calculations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                calculator_type TEXT NOT NULL,
                input_data TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def save_calculation(calculator_type: str, input_data: str, result: str):
    """Save a calculation to the database."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO calculations (calculator_type, input_data, result) VALUES (?, ?, ?)",
            (calculator_type, input_data, result)
        )
        await db.commit()

async def get_history(limit: int = 10):
    """Get recent calculation history."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM calculations ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        return await cursor.fetchall()

# ============================================================================
# FASTAPI APP SETUP
# ============================================================================

app = FastAPI(title="Calculator Hub", description="Beautiful Multi-Calculator Web App")

# Create templates directory
Path("templates").mkdir(exist_ok=True)

# ============================================================================
# HTML TEMPLATE
# ============================================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculator Hub - Универсальные Калькуляторы</title>
    <style>
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --secondary: #ec4899;
            --accent: #06b6d4;
            --bg-dark: #0f172a;
            --bg-card: #1e293b;
            --bg-input: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --success: #10b981;
            --warning: #f59e0b;
            --border-radius: 16px;
            --shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, var(--bg-dark) 0%, #1e1b4b 100%);
            min-height: 100vh;
            color: var(--text-primary);
            overflow-x: hidden;
        }

        /* Animated Background */
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            overflow: hidden;
        }

        .bg-animation span {
            position: absolute;
            display: block;
            width: 20px;
            height: 20px;
            background: rgba(99, 102, 241, 0.1);
            animation: move 25s infinite;
            bottom: -150px;
            border-radius: 50%;
        }

        .bg-animation span:nth-child(1) { left: 25%; width: 80px; height: 80px; animation-delay: 0s; }
        .bg-animation span:nth-child(2) { left: 10%; width: 20px; height: 20px; animation-delay: 2s; animation-duration: 12s; }
        .bg-animation span:nth-child(3) { left: 70%; width: 20px; height: 20px; animation-delay: 4s; }
        .bg-animation span:nth-child(4) { left: 40%; width: 60px; height: 60px; animation-delay: 0s; animation-duration: 18s; }
        .bg-animation span:nth-child(5) { left: 65%; width: 20px; height: 20px; animation-delay: 0s; }
        .bg-animation span:nth-child(6) { left: 75%; width: 110px; height: 110px; animation-delay: 3s; }
        .bg-animation span:nth-child(7) { left: 35%; width: 150px; height: 150px; animation-delay: 7s; }
        .bg-animation span:nth-child(8) { left: 50%; width: 25px; height: 25px; animation-delay: 15s; animation-duration: 45s; }
        .bg-animation span:nth-child(9) { left: 20%; width: 15px; height: 15px; animation-delay: 2s; animation-duration: 35s; }
        .bg-animation span:nth-child(10) { left: 85%; width: 150px; height: 150px; animation-delay: 0s; animation-duration: 11s; }

        @keyframes move {
            0% { transform: translateY(0) rotate(0deg); opacity: 1; border-radius: 50%; }
            100% { transform: translateY(-1000px) rotate(720deg); opacity: 0; border-radius: 50%; }
        }

        /* Header */
        header {
            text-align: center;
            padding: 3rem 1rem;
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        h1 {
            font-size: 3rem;
            background: linear-gradient(135deg, var(--primary), var(--secondary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            animation: glow 2s ease-in-out infinite alternate;
        }

        @keyframes glow {
            from { filter: drop-shadow(0 0 20px rgba(99, 102, 241, 0.5)); }
            to { filter: drop-shadow(0 0 30px rgba(236, 72, 153, 0.5)); }
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 1.1rem;
        }

        /* Container */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        /* Tabs */
        .tabs {
            display: flex;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            justify-content: center;
        }

        .tab-btn {
            padding: 1rem 2rem;
            background: var(--bg-card);
            border: 2px solid transparent;
            border-radius: var(--border-radius);
            color: var(--text-primary);
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .tab-btn:hover {
            background: var(--bg-input);
            transform: translateY(-2px);
        }

        .tab-btn.active {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-color: var(--primary);
            box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
        }

        .tab-btn .icon {
            font-size: 1.3rem;
        }

        /* Tab Content */
        .tab-content {
            display: none;
            animation: fadeIn 0.5s ease;
        }

        .tab-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Cards */
        .card {
            background: var(--bg-card);
            border-radius: var(--border-radius);
            padding: 2rem;
            box-shadow: var(--shadow);
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 2rem;
        }

        .card h2 {
            font-size: 1.8rem;
            margin-bottom: 1.5rem;
            color: var(--primary);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Forms */
        .form-group {
            margin-bottom: 1.5rem;
        }

        label {
            display: block;
            margin-bottom: 0.5rem;
            color: var(--text-secondary);
            font-weight: 500;
        }

        input, select, textarea {
            width: 100%;
            padding: 1rem;
            background: var(--bg-input);
            border: 2px solid transparent;
            border-radius: 12px;
            color: var(--text-primary);
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        input:focus, select:focus, textarea:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
        }

        input[type="number"] {
            -moz-appearance: textfield;
        }

        input[type="number"]::-webkit-inner-spin-button,
        input[type="number"]::-webkit-outer-spin-button {
            -webkit-appearance: none;
            margin: 0;
        }

        /* Buttons */
        .btn {
            padding: 1rem 2rem;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none;
            border-radius: 12px;
            color: white;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 35px rgba(99, 102, 241, 0.4);
        }

        .btn:active {
            transform: translateY(-1px);
        }

        .btn-full {
            width: 100%;
            justify-content: center;
        }

        /* Result Box */
        .result-box {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(6, 182, 212, 0.1));
            border: 2px solid var(--success);
            border-radius: 12px;
            padding: 1.5rem;
            margin-top: 1.5rem;
            display: none;
            animation: slideIn 0.5s ease;
        }

        .result-box.show {
            display: block;
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }

        .result-box h3 {
            color: var(--success);
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .result-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        .result-details {
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        /* History Section */
        .history-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }

        .history-item {
            background: var(--bg-input);
            padding: 1rem;
            border-radius: 12px;
            border-left: 4px solid var(--primary);
            animation: fadeIn 0.3s ease;
        }

        .history-item .type {
            color: var(--primary);
            font-weight: 600;
            font-size: 0.85rem;
            margin-bottom: 0.5rem;
        }

        .history-item .result {
            color: var(--success);
            font-weight: 700;
            font-size: 1.1rem;
        }

        .history-item .time {
            color: var(--text-secondary);
            font-size: 0.8rem;
            margin-top: 0.5rem;
        }

        /* Info Cards */
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }

        .info-card {
            background: var(--bg-input);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
        }

        .info-card:hover {
            transform: translateY(-5px);
            border-color: var(--primary);
            box-shadow: 0 10px 30px rgba(99, 102, 241, 0.2);
        }

        .info-card h3 {
            color: var(--accent);
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .info-card p {
            color: var(--text-secondary);
            line-height: 1.6;
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 2rem;
            color: var(--text-secondary);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            margin-top: 3rem;
        }

        /* Responsive */
        @media (max-width: 768px) {
            h1 { font-size: 2rem; }
            .tabs { flex-direction: column; }
            .tab-btn { width: 100%; justify-content: center; }
            .container { padding: 1rem; }
        }

        /* Loading Animation */
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <!-- Background Animation -->
    <div class="bg-animation">
        <span></span><span></span><span></span><span></span><span></span>
        <span></span><span></span><span></span><span></span><span></span>
    </div>

    <!-- Header -->
    <header>
        <h1>🧮 Calculator Hub</h1>
        <p class="subtitle">Универсальные калькуляторы для всех случаев жизни</p>
    </header>

    <!-- Main Container -->
    <div class="container">
        <!-- Navigation Tabs -->
        <div class="tabs">
            <button class="tab-btn active" data-tab="math">
                <span class="icon">📐</span> Математический
            </button>
            <button class="tab-btn" data-tab="finance">
                <span class="icon">💰</span> Финансовый
            </button>
            <button class="tab-btn" data-tab="health">
                <span class="icon">❤️</span> Здоровье
            </button>
            <button class="tab-btn" data-tab="convert">
                <span class="icon">🔄</span> Конвертер
            </button>
            <button class="tab-btn" data-tab="history">
                <span class="icon">📊</span> История
            </button>
            <button class="tab-btn" data-tab="about">
                <span class="icon">ℹ️</span> О приложении
            </button>
        </div>

        <!-- Math Calculator Tab -->
        <div id="math" class="tab-content active">
            <div class="card">
                <h2>📐 Математический Калькулятор</h2>
                <form id="math-form">
                    <div class="form-group">
                        <label>Выберите операцию</label>
                        <select name="operation" required>
                            <option value="addition">Сложение (+)</option>
                            <option value="subtraction">Вычитание (-)</option>
                            <option value="multiplication">Умножение (×)</option>
                            <option value="division">Деление (÷)</option>
                            <option value="power">Возведение в степень (^)</option>
                            <option value="sqrt">Квадратный корень (√)</option>
                            <option value="factorial">Факториал (!)</option>
                            <option value="sin">Синус (sin)</option>
                            <option value="cos">Косинус (cos)</option>
                            <option value="tan">Тангенс (tan)</option>
                            <option value="log">Логарифм (log₁₀)</option>
                        </select>
                    </div>
                    <div class="form-group" id="input-two-fields">
                        <label>Первое число</label>
                        <input type="number" name="num1" step="any" placeholder="Введите число">
                    </div>
                    <div class="form-group" id="input-one-field" style="display:none;">
                        <label>Число</label>
                        <input type="number" name="num1" step="any" placeholder="Введите число">
                    </div>
                    <div class="form-group" id="input-second-field">
                        <label>Второе число</label>
                        <input type="number" name="num2" step="any" placeholder="Введите число">
                    </div>
                    <button type="submit" class="btn btn-full">
                        <span>🚀</span> Рассчитать
                    </button>
                </form>
                <div class="result-box" id="math-result">
                    <h3>✅ Результат:</h3>
                    <div class="result-value" id="math-result-value"></div>
                    <div class="result-details" id="math-result-details"></div>
                </div>
            </div>
        </div>

        <!-- Finance Calculator Tab -->
        <div id="finance" class="tab-content">
            <div class="card">
                <h2>💰 Финансовый Калькулятор</h2>
                <form id="finance-form">
                    <div class="form-group">
                        <label>Тип расчета</label>
                        <select name="calc_type" required>
                            <option value="compound">Сложный процент</option>
                            <option value="loan">Ежемесячный платеж по кредиту</option>
                            <option value="roi">ROI (Возврат инвестиций)</option>
                            <option value="vat">НДС (20%)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Основная сумма (₽)</label>
                        <input type="number" name="principal" step="any" placeholder="100000" required>
                    </div>
                    <div class="form-group" id="finance-rate-group">
                        <label>Процентная ставка (% годовых)</label>
                        <input type="number" name="rate" step="any" placeholder="10">
                    </div>
                    <div class="form-group" id="finance-period-group">
                        <label>Срок (лет)</label>
                        <input type="number" name="period" step="any" placeholder="5">
                    </div>
                    <button type="submit" class="btn btn-full">
                        <span>💵</span> Рассчитать
                    </button>
                </form>
                <div class="result-box" id="finance-result">
                    <h3>✅ Результат:</h3>
                    <div class="result-value" id="finance-result-value"></div>
                    <div class="result-details" id="finance-result-details"></div>
                </div>
            </div>
        </div>

        <!-- Health Calculator Tab -->
        <div id="health" class="tab-content">
            <div class="card">
                <h2>❤️ Калькулятор Здоровья</h2>
                <form id="health-form">
                    <div class="form-group">
                        <label>Тип расчета</label>
                        <select name="health_type" required>
                            <option value="bmi">ИМТ (Индекс массы тела)</option>
                            <option value="bmr">BMR (Базальный метаболизм)</option>
                            <option value="water">Норма воды в день</option>
                            <option value="calories">Калории для похудения</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Вес (кг)</label>
                        <input type="number" name="weight" step="any" placeholder="70" required>
                    </div>
                    <div class="form-group">
                        <label>Рост (см)</label>
                        <input type="number" name="height" step="any" placeholder="175">
                    </div>
                    <div class="form-group">
                        <label>Возраст (лет)</label>
                        <input type="number" name="age" step="any" placeholder="30">
                    </div>
                    <div class="form-group">
                        <label>Пол</label>
                        <select name="gender">
                            <option value="male">Мужской</option>
                            <option value="female">Женский</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Уровень активности</label>
                        <select name="activity">
                            <option value="1.2">Минимальный (сидячая работа)</option>
                            <option value="1.375">Низкий (легкие упражнения 1-3 дня)</option>
                            <option value="1.55">Средний (умеренные упражнения 3-5 дней)</option>
                            <option value="1.725">Высокий (интенсивные упражнения 6-7 дней)</option>
                            <option value="1.9">Экстремальный (тяжелая физическая работа)</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-full">
                        <span>💪</span> Рассчитать
                    </button>
                </form>
                <div class="result-box" id="health-result">
                    <h3>✅ Результат:</h3>
                    <div class="result-value" id="health-result-value"></div>
                    <div class="result-details" id="health-result-details"></div>
                </div>
            </div>
        </div>

        <!-- Converter Tab -->
        <div id="convert" class="tab-content">
            <div class="card">
                <h2>🔄 Конвертер Величин</h2>
                <form id="convert-form">
                    <div class="form-group">
                        <label>Тип конвертации</label>
                        <select name="convert_type" required>
                            <option value="length">Длина</option>
                            <option value="weight">Вес</option>
                            <option value="temperature">Температура</option>
                            <option value="speed">Скорость</option>
                            <option value="data">Объем данных</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Из единицы</label>
                        <select name="from_unit" id="from-unit" required></select>
                    </div>
                    <div class="form-group">
                        <label>В единицу</label>
                        <select name="to_unit" id="to-unit" required></select>
                    </div>
                    <div class="form-group">
                        <label>Значение</label>
                        <input type="number" name="value" step="any" placeholder="100" required>
                    </div>
                    <button type="submit" class="btn btn-full">
                        <span>🔄</span> Конвертировать
                    </button>
                </form>
                <div class="result-box" id="convert-result">
                    <h3>✅ Результат:</h3>
                    <div class="result-value" id="convert-result-value"></div>
                    <div class="result-details" id="convert-result-details"></div>
                </div>
            </div>
        </div>

        <!-- History Tab -->
        <div id="history" class="tab-content">
            <div class="card">
                <h2>📊 История Расчетов</h2>
                <p style="color: var(--text-secondary); margin-bottom: 1rem;">
                    Последние 10 расчетов сохраняются автоматически
                </p>
                <div class="history-grid" id="history-list">
                    <p style="color: var(--text-secondary);">Загрузка истории...</p>
                </div>
                <button onclick="loadHistory()" class="btn" style="margin-top: 1rem;">
                    <span>🔄</span> Обновить
                </button>
            </div>
        </div>

        <!-- About Tab -->
        <div id="about" class="tab-content">
            <div class="card">
                <h2>ℹ️ О Приложении</h2>
                <p style="color: var(--text-secondary); line-height: 1.8; margin-bottom: 1.5rem;">
                    <strong>Calculator Hub</strong> — это универсальное веб-приложение с набором полезных калькуляторов 
                    для повседневных задач. Приложение построено на современном стеке технологий и предлагает 
                    красивый интерфейс с плавными анимациями.
                </p>
                
                <div class="info-grid">
                    <div class="info-card">
                        <h3>📐 Математика</h3>
                        <p>Базовые арифметические операции, тригонометрические функции, факториалы и логарифмы.</p>
                    </div>
                    <div class="info-card">
                        <h3>💰 Финансы</h3>
                        <p>Расчет сложных процентов, кредитных платежей, ROI и НДС для финансового планирования.</p>
                    </div>
                    <div class="info-card">
                        <h3>❤️ Здоровье</h3>
                        <p>ИМТ, базальный метаболизм, норма воды и калории для здорового образа жизни.</p>
                    </div>
                    <div class="info-card">
                        <h3>🔄 Конвертер</h3>
                        <p>Конвертация между различными единицами измерения: длина, вес, температура, скорость, данные.</p>
                    </div>
                </div>

                <div style="margin-top: 2rem; padding: 1.5rem; background: var(--bg-input); border-radius: 12px;">
                    <h3 style="color: var(--primary); margin-bottom: 1rem;">🛠 Технологии</h3>
                    <ul style="color: var(--text-secondary); line-height: 2;">
                        <li><strong>Backend:</strong> Python + FastAPI</li>
                        <li><strong>Database:</strong> SQLite (файловая БД)</li>
                        <li><strong>Frontend:</strong> HTML5, CSS3, Vanilla JavaScript</li>
                        <li><strong>Анимации:</strong> CSS Keyframes & Transitions</li>
                    </ul>
                </div>

                <div style="margin-top: 1.5rem; text-align: center; color: var(--text-secondary);">
                    <p>Сделано с ❤️ для удобства пользователей</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer>
        <p>&copy; 2024 Calculator Hub. Все права защищены.</p>
    </footer>

    <script>
        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                btn.classList.add('active');
                document.getElementById(btn.dataset.tab).classList.add('active');
                
                if (btn.dataset.tab === 'history') {
                    loadHistory();
                }
            });
        });

        // Math form field visibility
        const mathForm = document.getElementById('math-form');
        const operationSelect = mathForm.querySelector('select[name="operation"]');
        
        function updateMathFields() {
            const singleOps = ['sqrt', 'factorial', 'sin', 'cos', 'tan', 'log'];
            const isSingle = singleOps.includes(operationSelect.value);
            
            document.getElementById('input-two-fields').style.display = isSingle ? 'none' : 'block';
            document.getElementById('input-one-field').style.display = isSingle ? 'block' : 'none';
            document.getElementById('input-second-field').style.display = isSingle ? 'none' : 'block';
        }
        
        operationSelect.addEventListener('change', updateMathFields);
        updateMathFields();

        // Finance form field visibility
        const financeForm = document.getElementById('finance-form');
        const financeTypeSelect = financeForm.querySelector('select[name="calc_type"]');
        
        function updateFinanceFields() {
            const needsRatePeriod = ['compound', 'loan'].includes(financeTypeSelect.value);
            document.getElementById('finance-rate-group').style.display = needsRatePeriod ? 'block' : 'none';
            document.getElementById('finance-period-group').style.display = needsRatePeriod ? 'block' : 'none';
            
            const rateInput = financeForm.querySelector('input[name="rate"]');
            const periodInput = financeForm.querySelector('input[name="period"]');
            rateInput.required = needsRatePeriod;
            periodInput.required = needsRatePeriod;
        }
        
        financeTypeSelect.addEventListener('change', updateFinanceFields);
        updateFinanceFields();

        // Unit options for converter
        const unitOptions = {
            length: {
                m: 'Метры', km: 'Километры', cm: 'Сантиметры', mm: 'Миллиметры', 
                ft: 'Футы', in: 'Дюймы', mi: 'Мили', yd: 'Ярды'
            },
            weight: {
                kg: 'Килограммы', g: 'Граммы', mg: 'Миллиграммы', 
                lb: 'Фунты', oz: 'Унции', t: 'Тонны'
            },
            temperature: {
                c: 'Цельсий', f: 'Фаренгейт', k: 'Кельвин'
            },
            speed: {
                ms: 'м/с', kmh: 'км/ч', mph: 'mph', kn: 'Узлы'
            },
            data: {
                b: 'Байты', kb: 'Килобайты', mb: 'Мегабайты', gb: 'Гигабайты', tb: 'Терабайты'
            }
        };

        const convertTypeSelect = document.getElementById('convert-form').querySelector('select[name="convert_type"]');
        const fromUnitSelect = document.getElementById('from-unit');
        const toUnitSelect = document.getElementById('to-unit');

        function updateUnitOptions() {
            const type = convertTypeSelect.value;
            const units = unitOptions[type];
            
            fromUnitSelect.innerHTML = '';
            toUnitSelect.innerHTML = '';
            
            for (const [key, value] of Object.entries(units)) {
                fromUnitSelect.add(new Option(value, key));
                toUnitSelect.add(new Option(value, key));
            }
            
            if (Object.keys(units).length > 1) {
                toUnitSelect.selectedIndex = 1;
            }
        }

        convertTypeSelect.addEventListener('change', updateUnitOptions);
        updateUnitOptions();

        // Show result helper
        function showResult(containerId, value, details) {
            const container = document.getElementById(containerId);
            document.getElementById(containerId + '-value').textContent = value;
            document.getElementById(containerId + '-details').innerHTML = details;
            container.classList.add('show');
            container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

        // Math calculator
        mathForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(mathForm);
            
            try {
                const response = await fetch('/api/calculate/math', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams(formData)
                });
                
                const data = await response.json();
                if (data.success) {
                    showResult('math-result', data.result.value, data.result.details);
                } else {
                    alert('Ошибка: ' + data.error);
                }
            } catch (error) {
                alert('Ошибка соединения: ' + error.message);
            }
        });

        // Finance calculator
        financeForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(financeForm);
            
            try {
                const response = await fetch('/api/calculate/finance', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams(formData)
                });
                
                const data = await response.json();
                if (data.success) {
                    showResult('finance-result', data.result.value, data.result.details);
                } else {
                    alert('Ошибка: ' + data.error);
                }
            } catch (error) {
                alert('Ошибка соединения: ' + error.message);
            }
        });

        // Health calculator
        document.getElementById('health-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            
            try {
                const response = await fetch('/api/calculate/health', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams(formData)
                });
                
                const data = await response.json();
                if (data.success) {
                    showResult('health-result', data.result.value, data.result.details);
                } else {
                    alert('Ошибка: ' + data.error);
                }
            } catch (error) {
                alert('Ошибка соединения: ' + error.message);
            }
        });

        // Converter
        document.getElementById('convert-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            
            try {
                const response = await fetch('/api/calculate/convert', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: new URLSearchParams(formData)
                });
                
                const data = await response.json();
                if (data.success) {
                    showResult('convert-result', data.result.value, data.result.details);
                } else {
                    alert('Ошибка: ' + data.error);
                }
            } catch (error) {
                alert('Ошибка соединения: ' + error.message);
            }
        });

        // Load history
        async function loadHistory() {
            try {
                const response = await fetch('/api/history');
                const data = await response.json();
                
                const historyList = document.getElementById('history-list');
                
                if (data.length === 0) {
                    historyList.innerHTML = '<p style="color: var(--text-secondary); grid-column: 1/-1; text-align: center;">История пуста</p>';
                    return;
                }
                
                historyList.innerHTML = data.map(item => `
                    <div class="history-item">
                        <div class="type">${item.calculator_type}</div>
                        <div class="result">${item.result}</div>
                        <div class="time">${new Date(item.created_at).toLocaleString('ru-RU')}</div>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Error loading history:', error);
            }
        }

        // Auto-hide results after 30 seconds
        setInterval(() => {
            document.querySelectorAll('.result-box').forEach(box => {
                box.classList.remove('show');
            });
        }, 30000);
    </script>
</body>
</html>
"""

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main HTML page."""
    return HTMLResponse(content=HTML_TEMPLATE)

@app.post("/api/calculate/math")
async def calculate_math(
    operation: str = Form(...),
    num1: float = Form(...),
    num2: Optional[float] = Form(None)
):
    """Perform mathematical calculations."""
    try:
        single_ops = ['sqrt', 'factorial', 'sin', 'cos', 'tan', 'log']
        
        if operation in single_ops and num2 is not None:
            num2 = None
        
        result = 0
        details = ""
        
        if operation == 'addition':
            result = num1 + num2
            details = f"{num1} + {num2} = {result}"
        elif operation == 'subtraction':
            result = num1 - num2
            details = f"{num1} - {num2} = {result}"
        elif operation == 'multiplication':
            result = num1 * num2
            details = f"{num1} × {num2} = {result}"
        elif operation == 'division':
            if num2 == 0:
                return {"success": False, "error": "Деление на ноль невозможно"}
            result = num1 / num2
            details = f"{num1} ÷ {num2} = {result}"
        elif operation == 'power':
            result = num1 ** num2
            details = f"{num1} ^ {num2} = {result}"
        elif operation == 'sqrt':
            if num1 < 0:
                return {"success": False, "error": "Корень из отрицательного числа не определен"}
            result = math.sqrt(num1)
            details = f"√{num1} = {result}"
        elif operation == 'factorial':
            if num1 < 0 or num1 != int(num1):
                return {"success": False, "error": "Факториал определен только для неотрицательных целых чисел"}
            result = math.factorial(int(num1))
            details = f"{int(num1)}! = {result}"
        elif operation == 'sin':
            result = math.sin(math.radians(num1))
            details = f"sin({num1}°) = {result}"
        elif operation == 'cos':
            result = math.cos(math.radians(num1))
            details = f"cos({num1}°) = {result}"
        elif operation == 'tan':
            result = math.tan(math.radians(num1))
            details = f"tan({num1}°) = {result}"
        elif operation == 'log':
            if num1 <= 0:
                return {"success": False, "error": "Логарифм определен только для положительных чисел"}
            result = math.log10(num1)
            details = f"log₁₀({num1}) = {result}"
        
        await save_calculation("Математика", details, str(result))
        
        return {
            "success": True,
            "result": {
                "value": f"{result:.6f}".rstrip('0').rstrip('.') if isinstance(result, float) else str(result),
                "details": details
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/calculate/finance")
async def calculate_finance(
    calc_type: str = Form(...),
    principal: float = Form(...),
    rate: Optional[float] = Form(None),
    period: Optional[float] = Form(None)
):
    """Perform financial calculations."""
    try:
        result = 0
        details = ""
        
        if calc_type == 'compound':
            if rate is None or period is None:
                return {"success": False, "error": "Требуется ставка и период"}
            result = principal * ((1 + rate / 100) ** period)
            interest = result - principal
            details = f"Initial: {principal:,.2f}₽ | Rate: {rate}% | Period: {period} years<br>Final: {result:,.2f}₽ | Interest: {interest:,.2f}₽"
        
        elif calc_type == 'loan':
            if rate is None or period is None:
                return {"success": False, "error": "Требуется ставка и период"}
            monthly_rate = rate / 100 / 12
            months = period * 12
            if monthly_rate > 0:
                result = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
            else:
                result = principal / months
            total_payment = result * months
            total_interest = total_payment - principal
            details = f"Loan: {principal:,.2f}₽ | Rate: {rate}% | Period: {period} years<br>Monthly: {result:,.2f}₽ | Total: {total_payment:,.2f}₽ | Interest: {total_interest:,.2f}₽"
        
        elif calc_type == 'roi':
            if rate is None:
                return {"success": False, "error": "Требуется процент возврата"}
            result = principal * (rate / 100)
            total = principal + result
            details = f"Investment: {principal:,.2f}₽ | Return: {rate}%<br>Profit: {result:,.2f}₽ | Total: {total:,.2f}₽"
        
        elif calc_type == 'vat':
            vat_rate = 20
            vat_amount = principal * vat_rate / 100
            result = vat_amount
            total = principal + vat_amount
            details = f"Amount: {principal:,.2f}₽ | VAT ({vat_rate}%): {vat_amount:,.2f}₽<br>Total with VAT: {total:,.2f}₽"
        
        await save_calculation("Финансы", f"{calc_type}: {principal}", str(result))
        
        return {
            "success": True,
            "result": {
                "value": f"{result:,.2f}₽",
                "details": details
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/calculate/health")
async def calculate_health(
    health_type: str = Form(...),
    weight: float = Form(...),
    height: Optional[float] = Form(None),
    age: Optional[float] = Form(None),
    gender: str = Form("male"),
    activity: float = Form(1.2)
):
    """Perform health-related calculations."""
    try:
        result = 0
        value = ""
        details = ""
        
        if health_type == 'bmi':
            if height is None or height == 0:
                return {"success": False, "error": "Требуется рост"}
            height_m = height / 100
            result = weight / (height_m ** 2)
            
            if result < 18.5:
                category = "Недостаточный вес"
                color = "#f59e0b"
            elif result < 25:
                category = "Нормальный вес"
                color = "#10b981"
            elif result < 30:
                category = "Избыточный вес"
                color = "#f59e0b"
            else:
                category = "Ожирение"
                color = "#ef4444"
            
            value = f"{result:.1f}"
            details = f"Weight: {weight}kg | Height: {height}cm<br>Category: <span style='color: {color}'>{category}</span>"
        
        elif health_type == 'bmr':
            if height is None or age is None:
                return {"success": False, "error": "Требуются рост и возраст"}
            
            if gender == 'male':
                result = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                result = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            
            tdee = result * activity
            value = f"{result:.0f} ккал"
            details = f"BMR: {result:.0f} ккал/день<br>TDEE (with activity): {tdee:.0f} ккал/день"
        
        elif health_type == 'water':
            result = weight * 0.033
            value = f"{result:.2f} л"
            details = f"Recommended daily water intake based on weight"
        
        elif health_type == 'calories':
            if height is None or age is None:
                return {"success": False, "error": "Требуются рост и возраст"}
            
            if gender == 'male':
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            
            tdee = bmr * activity
            loss_calories = tdee - 500
            gain_calories = tdee + 500
            
            value = f"{tdee:.0f} ккал"
            details = f"Maintenance: {tdee:.0f} ккал/день<br>Weight loss: {loss_calories:.0f} ккал/день (-0.5kg/week)<br>Weight gain: {gain_calories:.0f} ккал/день (+0.5kg/week)"
        
        await save_calculation("Здоровье", f"{health_type}: {weight}kg", str(result))
        
        return {
            "success": True,
            "result": {
                "value": value,
                "details": details
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/calculate/convert")
async def convert_units(
    convert_type: str = Form(...),
    from_unit: str = Form(...),
    to_unit: str = Form(...),
    value: float = Form(...)
):
    """Convert between different units."""
    try:
        result = 0
        details = ""
        
        # Conversion rates to base unit
        conversions = {
            'length': {
                'm': 1, 'km': 1000, 'cm': 0.01, 'mm': 0.001,
                'ft': 0.3048, 'in': 0.0254, 'mi': 1609.34, 'yd': 0.9144
            },
            'weight': {
                'kg': 1, 'g': 0.001, 'mg': 0.000001,
                'lb': 0.453592, 'oz': 0.0283495, 't': 1000
            },
            'speed': {
                'ms': 1, 'kmh': 0.277778, 'mph': 0.44704, 'kn': 0.514444
            },
            'data': {
                'b': 1, 'kb': 1024, 'mb': 1048576, 'gb': 1073741824, 'tb': 1099511627776
            }
        }
        
        if convert_type == 'temperature':
            temp_conversions = {
                ('c', 'f'): lambda x: x * 9/5 + 32,
                ('c', 'k'): lambda x: x + 273.15,
                ('f', 'c'): lambda x: (x - 32) * 5/9,
                ('f', 'k'): lambda x: (x - 32) * 5/9 + 273.15,
                ('k', 'c'): lambda x: x - 273.15,
                ('k', 'f'): lambda x: (x - 273.15) * 9/5 + 32,
            }
            
            if from_unit == to_unit:
                result = value
            else:
                result = temp_conversions[(from_unit, to_unit)](value)
            
            unit_names = {'c': '°C', 'f': '°F', 'k': 'K'}
            details = f"{value} {unit_names[from_unit]} = {result:.2f} {unit_names[to_unit]}"
        
        elif convert_type in conversions:
            rates = conversions[convert_type]
            base_value = value * rates[from_unit]
            result = base_value / rates[to_unit]
            details = f"{value} {from_unit} = {result:.6f} {to_unit}"
        
        await save_calculation("Конвертер", f"{value} {from_unit} → {to_unit}", str(result))
        
        return {
            "success": True,
            "result": {
                "value": f"{result:.6f}".rstrip('0').rstrip('.'),
                "details": details
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/history")
async def get_calculation_history():
    """Get calculation history."""
    history = await get_history(10)
    return [dict(row) for row in history]

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the application."""
    print("=" * 60)
    print("🧮 Calculator Hub - Запуск приложения")
    print("=" * 60)
    print()
    
    # Initialize database
    asyncio.run(init_db())
    print("✅ База данных инициализирована")
    print()
    
    print(f"🌐 Откройте в браузере: http://{HOST}:{PORT}")
    print()
    print("⏹️  Для остановки нажмите: Ctrl+C")
    print("=" * 60)
    print()
    
    # Start server
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")

if __name__ == "__main__":
    main()
