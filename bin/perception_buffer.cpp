#include <iostream>
#include <string>
#include <sqlite3.h>
#include <ctime>
#include <cstdlib>
#include <iomanip>

double get_vault_metric(const std::string& metric_name) {
    sqlite3* db = nullptr;
    sqlite3_stmt* stmt = nullptr;
    double value = 0.0;
    const char* home = getenv("HOME");
    if (!home) return 0.0;
    std::string path = std::string(home) + "/shmry_cloud_hyperscale/vault/shmry_cloud.db"; 

    if (sqlite3_open(path.c_str(), &db) == SQLITE_OK) {
        sqlite3_busy_timeout(db, 2000);
        const char* query = "SELECT value FROM sovereign_metrics WHERE name = ?;";
        if (sqlite3_prepare_v2(db, query, -1, &stmt, nullptr) == SQLITE_OK) {
            sqlite3_bind_text(stmt, 1, metric_name.c_str(), -1, SQLITE_TRANSIENT);
            if (sqlite3_step(stmt) == SQLITE_ROW) {
                value = sqlite3_column_double(stmt, 0);
            }
            sqlite3_finalize(stmt);
        }
        sqlite3_close(db);
    }
    return value;
}

int main(int argc, char* argv[]) {
    if (argc > 1 && std::string(argv[1]) == "HEALTH_CHECK") {
        double vol = get_vault_metric("market_volatility");
        double css = get_vault_metric("css_mastery"); 
        double fuel = get_vault_metric("rangoons_fuel"); 
        
        time_t t = time(0);
        struct tm * now = localtime(&t);
        
        std::string status;
        std::string directive = "EVOLVE";

        // Logic Tiering
        if (vol >= 0.70) {
            status = "VOLATILITY_GUARD";
            directive = "HOLD_POSITION";
        } else if (vol < 0.20 && fuel > 0.90) {
            status = "AGGRESSIVE_GROWTH";
            directive = "EVOLVE";
        } else {
            status = "STABLE_OBSERVATION";
            directive = "MONITOR";
        }

        std::cout << "{"
                  << "\"status\":\"" << status << "\","
                  << "\"engine\":\"NIFDU-CPP-CORE\","
                  << "\"hour\":" << (now ? now->tm_hour : -1) << ","
                  << "\"css_mastery\":" << css << ","
                  << "\"rangoons_fuel\":" << fuel << ","
                  << "\"market_volatility\":" << std::fixed << std::setprecision(2) << vol << ","
                  << "\"directive\":\"" << directive << "\""
                  << "}" << std::endl;
    }
    return 0;
}
