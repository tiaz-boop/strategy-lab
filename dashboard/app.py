import sqlite3, json
from flask import Flask, jsonify, render_template

def create_app(db="strategy_lab.db"):
    app=Flask(__name__)
    def con():
        c=sqlite3.connect(db); c.row_factory=sqlite3.Row; return c

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/status")
    def status():
        c=con()
        q=c.execute("SELECT status,COUNT(*) n FROM experiments GROUP BY status").fetchall()
        top=c.execute("""SELECT s.id,v.score,v.test_return,v.profit_factor,
                         v.max_drawdown,s.lifecycle
                         FROM validations v JOIN strategies s ON s.id=v.strategy_id
                         ORDER BY v.score DESC LIMIT 20""").fetchall()
        return jsonify({"queue":[dict(x) for x in q],"top":[dict(x) for x in top]})
    return app

if __name__=="__main__":
    create_app().run(host="127.0.0.1",port=8000)
