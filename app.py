"""CodSoft AI Internship Portfolio Web App.

Browser-based demos for the three completed CodSoft AI internship tasks.
The web UI is an optional portfolio enhancement; the original CLI projects remain intact.
"""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from flask import Flask, jsonify, render_template_string, request

ROOT = Path(__file__).resolve().parent


def load_module(name, relative_path):
    path = ROOT / relative_path
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load {relative_path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


chatbot = load_module("chatbot", "Task-1-Rule-Based-Chatbot/chatbot.py")
tictactoe = load_module("tictactoe", "Task-2-Tic-Tac-Toe-AI/tic_tac_toe.py")
recommender = load_module("recommender", "Task-4-Recommendation-System/recommendation_system.py")

app = Flask(__name__)

PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CodSoft AI Project Lab</title>
<style>
:root{--bg:#0b1020;--card:#141b2d;--text:#eef2ff;--muted:#aab4cc;--accent:#7c9cff;--good:#61d095;--line:#2b3650}
*{box-sizing:border-box}body{margin:0;background:linear-gradient(135deg,#0b1020,#111a31);color:var(--text);font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}header{padding:42px 20px 28px;text-align:center}h1{margin:0 0 8px;font-size:38px}h2{margin-top:0}p{color:var(--muted)}.badge{display:inline-block;border:1px solid var(--line);padding:5px 10px;border-radius:999px;color:var(--accent);margin-bottom:12px}.container{max-width:1100px;margin:auto;padding:0 18px 50px}.tabs{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:18px}.tab{background:var(--card);color:var(--text);border:1px solid var(--line);padding:11px 15px;border-radius:10px;cursor:pointer}.tab.active{background:var(--accent);color:#081022;border-color:var(--accent);font-weight:700}.panel{display:none;background:rgba(20,27,45,.96);border:1px solid var(--line);border-radius:18px;padding:24px}.panel.active{display:block}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}@media(max-width:760px){.grid{grid-template-columns:1fr}h1{font-size:30px}}input,select{width:100%;padding:12px;border-radius:10px;border:1px solid var(--line);background:#0d1425;color:var(--text);margin:8px 0}button.action{padding:11px 16px;border:0;border-radius:10px;background:var(--accent);color:#081022;font-weight:700;cursor:pointer}.chat{height:310px;overflow:auto;background:#0d1425;border:1px solid var(--line);border-radius:12px;padding:14px;margin-bottom:12px}.msg{margin:8px 0;padding:9px 11px;border-radius:10px;max-width:85%}.user{margin-left:auto;background:#27385f}.bot{background:#1c2940}.muted{color:var(--muted)}.board{display:grid;grid-template-columns:repeat(3,90px);gap:8px;justify-content:center;margin:20px 0}.cell{height:90px;font-size:38px;background:#0d1425;border:1px solid var(--line);color:var(--text);border-radius:12px;cursor:pointer}.cell:disabled{cursor:not-allowed;opacity:.75}.status{text-align:center;font-weight:700;min-height:28px}.recommendations{display:grid;gap:10px;margin-top:15px}.rec{background:#0d1425;border:1px solid var(--line);padding:13px;border-radius:11px;display:flex;justify-content:space-between;gap:12px}.score{color:var(--good);font-weight:700}.footer{text-align:center;color:var(--muted);padding:25px}
</style></head>
<body>
<header><span class="badge">CodSoft Artificial Intelligence Internship</span><h1>AI Project Lab</h1><p>Interactive demonstrations for Task 1, Task 2 and Task 4.</p></header>
<div class="container">
<div class="tabs"><button class="tab active" data-panel="chat">Task 1 · Chatbot</button><button class="tab" data-panel="game">Task 2 · Tic-Tac-Toe AI</button><button class="tab" data-panel="rec">Task 4 · Recommendation</button></div>
<section id="chat" class="panel active"><div class="grid"><div><h2>Rule-Based Chatbot</h2><p>Responses come from the same predefined Python rules used by the CLI project.</p><div class="chat" id="chatbox"><div class="msg bot">Bot: Hello! How can I help you today?</div></div><div style="display:flex;gap:8px"><input id="chatInput" placeholder="Ask something..." onkeydown="if(event.key==='Enter')sendChat()"><button class="action" onclick="sendChat()">Send</button></div></div><div><h3>Try these</h3><p>hello<br>what is AI?<br>what is machine learning?<br>how does AI work?<br>what can you do?<br>thank you<br>bye</p></div></div></section>
<section id="game" class="panel"><h2>Tic-Tac-Toe AI</h2><p>You are <b>X</b>. The AI is <b>O</b>. This UI calls the same Minimax engine as Task 2.</p><div class="board" id="board"></div><div class="status" id="gameStatus"></div><div style="text-align:center"><button class="action" onclick="newGame()">New Game</button></div></section>
<section id="rec" class="panel"><div class="grid"><div><h2>Movie Recommendation System</h2><p>Choose a movie and receive content-based recommendations using genre and keyword similarity.</p><select id="movieSelect"><option value="">Select a movie...</option></select><button class="action" onclick="recommend()">Recommend</button><div id="recs" class="recommendations"></div></div><div><h3>Explainable recommendations</h3><p>The Python recommender builds a profile from genres and keywords and ranks other movies using a cosine-style similarity score.</p><p class="muted">No black-box model is introduced; the original CodSoft task logic remains transparent and easy to explain.</p></div></div></section>
</div><div class="footer">CodSoft AI Internship · 3 completed task demos</div>
<script>
const tabs=document.querySelectorAll('.tab');tabs.forEach(t=>t.onclick=()=>{tabs.forEach(x=>x.classList.remove('active'));document.querySelectorAll('.panel').forEach(x=>x.classList.remove('active'));t.classList.add('active');document.getElementById(t.dataset.panel).classList.add('active')});
function escapeHtml(s){return String(s).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]))}
async function sendChat(){const input=document.getElementById('chatInput');const text=input.value.trim();if(!text)return;const box=document.getElementById('chatbox');box.innerHTML+=`<div class="msg user">You: ${escapeHtml(text)}</div>`;input.value='';const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text})});const d=await r.json();box.innerHTML+=`<div class="msg bot">Bot: ${escapeHtml(d.response)}</div>`;box.scrollTop=box.scrollHeight}
let board=[],gameFinished=false;
function newGame(){board=Array(9).fill(' ');gameFinished=false;renderBoard();document.getElementById('gameStatus').textContent='Your turn — choose a square.'}
function renderBoard(){const el=document.getElementById('board');el.innerHTML='';board.forEach((v,i)=>{const b=document.createElement('button');b.className='cell';b.textContent=v;b.disabled=v!==' '||gameFinished;b.onclick=()=>move(i);el.appendChild(b)})}
async function move(i){if(gameFinished||board[i]!==' ')return;board[i]='X';const r=await fetch('/api/tictactoe',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({board})});const d=await r.json();if(!r.ok){document.getElementById('gameStatus').textContent=d.error||'Invalid move.';return}board=d.board;gameFinished=d.game_over;document.getElementById('gameStatus').textContent=d.message;renderBoard()}
async function loadMovies(){const r=await fetch('/api/movies');const d=await r.json();const s=document.getElementById('movieSelect');d.movies.forEach(m=>{const o=document.createElement('option');o.value=m;o.textContent=m;s.appendChild(o)})}
async function recommend(){const title=document.getElementById('movieSelect').value;if(!title)return;const r=await fetch('/api/recommend',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title})});const d=await r.json();const el=document.getElementById('recs');if(!r.ok){el.innerHTML=`<div class="rec">${escapeHtml(d.error)}</div>`;return}el.innerHTML=d.recommendations.map(x=>`<div class="rec"><span>${escapeHtml(x.title)}</span><span class="score">${x.score}</span></div>`).join('')}
newGame();loadMovies();
</script></body></html>'''


@app.get("/")
def home():
    return render_template_string(PAGE)


@app.post("/api/chat")
def api_chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify(error="Please enter a message."), 400
    return jsonify(response=chatbot.get_response(message))


@app.post("/api/tictactoe")
def api_tictactoe():
    data = request.get_json(silent=True) or {}
    incoming = data.get("board", [])
    if not isinstance(incoming, list) or len(incoming) != 9:
        return jsonify(error="Invalid board."), 400
    if any(cell not in {"X", "O", " "} for cell in incoming):
        return jsonify(error="Invalid board values."), 400

    x_count, o_count = incoming.count("X"), incoming.count("O")
    if x_count != o_count + 1:
        return jsonify(error="Invalid turn state."), 400

    board = [incoming[i:i + 3] for i in range(0, 9, 3)]
    winner = tictactoe.check_winner(board)
    if winner or not tictactoe.available_moves(board):
        return jsonify(board=incoming, message="Game over. Start a new game.", game_over=True)

    move = tictactoe.best_ai_move(board)
    if move:
        board[move[0]][move[1]] = tictactoe.AI

    winner = tictactoe.check_winner(board)
    if winner == tictactoe.AI:
        message = "AI wins. Better luck next time!"
        game_over = True
    elif winner == tictactoe.HUMAN:
        message = "Congratulations! You won!"
        game_over = True
    elif not tictactoe.available_moves(board):
        message = "It's a draw!"
        game_over = True
    else:
        message = "Your turn — choose a square."
        game_over = False
    return jsonify(board=sum(board, []), message=message, game_over=game_over)


@app.get("/api/movies")
def api_movies():
    return jsonify(movies=[movie["title"] for movie in recommender.MOVIES])


@app.post("/api/recommend")
def api_recommend():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return jsonify(recommendations=[], error="Please select a movie."), 400
    selected, results = recommender.recommend(title)
    if selected is None:
        return jsonify(recommendations=[], error="Movie not found."), 404
    return jsonify(selected=selected["title"], recommendations=[{"title": movie_title, "score": f"{score:.2f}"} for score, movie_title in results])


if __name__ == "__main__":
    app.run(debug=True)
