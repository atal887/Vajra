#define ASIO_STANDALONE
#define CROW_MAIN
#include "crow_all.h"
#include <iostream>

// Middleware to force CORS headers on every single response
struct CORSMiddleware {
    struct context {};

    void before_handle(crow::request& req, crow::response& res, context& ctx) {
        // No action needed before the request
    }

    void after_handle(crow::request& req, crow::response& res, context& ctx) {
        res.add_header("Access-Control-Allow-Origin", "http://127.0.0.1:5500");
        res.add_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS");
        res.add_header("Access-Control-Allow-Headers", "Content-Type, Authorization");
    }
};

int main() {
    // We initialize the App with our Middleware struct
    crow::App<CORSMiddleware> app;

    CROW_ROUTE(app, "/search").methods("POST"_method, "OPTIONS"_method)
    ([&](const crow::request& req) {
        crow::response res;

        // 1. Handle Preflight explicitly
        if (req.method == "OPTIONS"_method) {
            res.code = 200;
            res.body = "OK";
            return res;
        }

        // 2. Main Logic for POST
        auto x = crow::json::load(req.body);
        if (!x || !x.has("nonce")) {
            // High difficulty for suspected bots (22)
            int difficulty = (x && x.has("is_bot") && x["is_bot"].b()) ? 22 : 3;
            
            crow::json::wvalue challenge;
            challenge["status"] = "CHALLENGE";
            challenge["seed"] = "MCD_TRAP_PROD";
            challenge["difficulty"] = difficulty;
            
            res.body = challenge.dump();
            res.code = 200;
        } else {
            std::cout << "[\033[1;32mVERIFIED\033[0m] Accessing Database..." << std::endl;
            res.body = "ACCESS GRANTED";
            res.code = 200;
        }
        return res;
    });

    std::cout << "MCD Defense Engine Running on Port 8085..." << std::endl;
    app.port(8085).run();
}