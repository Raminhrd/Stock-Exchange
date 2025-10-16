💹 Django Exchange Market API

A stock trading and order-matching simulation built with Django REST Framework.
Users can buy and sell company shares, manage their portfolios, and watch trades execute automatically when prices match.

🚀 Overview
👤 User System

Users can register and log in using JWT Authentication.
Upon registration, a user automatically receives login tokens.

Each user can:

Sign up and log in

Place buy or sell orders

View their current portfolio

See their personal trade history

🏢 Company System

The platform includes a list of companies whose shares can be traded.
Each company contains the following data:

Company name

Initial stock price

Current price (latest trade)

Total number of shares

Available shares for trading

Admins can add, edit, or remove companies through the Django Admin panel.

💰 Order System

Users can place buy or sell orders for company shares.
Each order includes the order type, share quantity, and price per share.

Order rules:

Price must stay within ±5% of the company’s current price.

Buy orders are sorted by highest price first.

Sell orders are sorted by lowest price first.

Each order has a defined status:

Active

Partially filled

Completed

⚖️ Automatic Matching Engine

This is the heart of the system 💹

Whenever an order is created, a signal checks whether there is an opposite order (buy/sell) that matches the criteria.

Trade logic:

If the buyer’s price equals or exceeds the seller’s price → a trade is executed ✅

If the buyer’s price is higher than the seller’s price → the trade happens at the buyer’s price ✅

If the buyer’s price is lower → no trade ❌

When a trade occurs:

Shares are transferred from the seller to the buyer

The company’s current price updates to the trade price

Order statuses are updated accordingly

A trade record is created and stored in the database

💼 Portfolio System

Each user has a portfolio showing their owned shares and average purchase price.
Whenever a trade occurs, the portfolios of both the buyer and seller are updated automatically.

For example:

When a user buys new shares, they are added to their holdings and the average price is recalculated.

When a user sells shares, the quantity decreases accordingly.

💹 Trade System

Every successful transaction is recorded in the system.
Each trade includes:

Buyer and seller information

The company involved

Trade price

Quantity of shares traded

Timestamp of the transaction

Users can view all trades in the market or only their own trade history.

🧠 System Flow

1️⃣ A user logs in with their JWT token.
2️⃣ The user places a buy or sell order.
3️⃣ The system automatically checks for matching orders and executes trades if conditions are met.
4️⃣ Shares are transferred between users, and the company’s price is updated.
5️⃣ The user can view their updated portfolio and trade history.

🔐 Authentication

The project uses SimpleJWT for authentication.
When users register, they immediately receive both access and refresh tokens.
Access tokens must be included in the request header to access protected endpoints like orders or portfolios.

🧩 Main API Endpoints

/api/accounts/signup/ → Register and receive tokens

/api/accounts/login/ → Log in and get tokens

/api/exchanges/companies/ → View companies and prices

/api/exchanges/orders/ → Create or list user orders

/api/exchanges/orders/active/ → View all active market orders

/api/exchanges/trades/ → List all trades in the market

/api/exchanges/my-trades/ → View user’s trade history

/api/exchanges/portfolio/ → View user’s holdings

🧾 Matching Logic Summary

The system continuously maintains an active list of buy and sell orders.

Sell orders are sorted from the lowest to highest price.

Buy orders are sorted from the highest to lowest price.

When prices match or overlap, a trade is executed automatically.

Once an order is fully filled, it is removed from the active list.

🧰 Tech Stack

Python 3.12+

Django 5+

Django REST Framework

SimpleJWT (JSON Web Tokens)

SQLite / PostgreSQL

Postman for API testing

💡 Developer Notes

All trade matching and updates are handled using Django Signals automatically — no manual trigger required.

Trades are performed safely within database transactions, ensuring data consistency even during concurrent orders.

The architecture is modular and extendable, allowing for future features like balance management or transaction fees.

🧾 Summary

The Django Exchange Market API is a complete stock trading simulation where users can place buy/sell orders and the system automatically executes trades based on market logic.
It’s designed for learning and practicing key backend development concepts, including:

Django Signals

REST API Architecture

Matching Engine Logic

JWT Authentication
