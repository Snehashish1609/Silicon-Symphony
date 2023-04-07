
const chatGPT = new Worker('http://127.0.0.1:5000//static//chatGPT.js');

const chatGPTResp = document.querySelector(".chatGPTResponse");

const arrowSend = document.querySelector(".sendButton");
const loadingDots = document.querySelector("#dots");
const loadingDot1 = document.querySelector("#dot1");
const loadingDot2 = document.querySelector("#dot2");
const loadingDot3 = document.querySelector("#dot3");

chatGPT.addEventListener('message', (event) => {
    loadingDots.style.display = "block";

    chatGPTResp.value = event.data;
    const newAnswerContainer = document.createElement("div");
    newAnswerContainer.className = "answerContainer";
    const newParagraph = document.createElement("p");
    newParagraph.className = "answer";
    newParagraph.innerHTML = event.data;
    newParagraph.style.width = `${event.data.length}ch`;
    newParagraph.style.WebkitAnimation = `typing 2s steps(${event.data.length}, end), blink-caret .3s steps(${event.data.length}, end) alternate`;
    newAnswerContainer.appendChild(newParagraph);

    const span = document.createElement("span");
    newAnswerContainer.appendChild(span);

    chatGPTResp.appendChild(newAnswerContainer);
    window.scrollTo(0, document.body.scrollHeight);

    arrowSend.style.display = "none";
    loadingDot1.style.animation = `load 1s steps(${event.data.length})`;

    loadingDot2.style.animation = `load 1s steps(${event.data.length})`;
    loadingDot2.style.animationDelay = `0.2s`;

    loadingDot3.style.animation = `load 1s steps(${event.data.length})`;
    loadingDot3.style.animationDelay = `0.4s`;
});

loadingDot3.addEventListener('animationend', function() {
    loadingDots.style.display = 'none';
    arrowSend.style.display = 'block';
});    

const chatGPTForm = document.querySelector(".chatForm");
chatGPTForm.addEventListener("submit", (e) => {    
    e.preventDefault();
    sendQuery();
});
const chatGPTQuestion = document.querySelector(".chatGPTQuestion");
const sendBtn = document.querySelector(".sendButton");
sendBtn.addEventListener("click", () => {
    sendQuery();
});

function sendQuery() {
    chatGPT.postMessage(chatGPTQuestion.value);
    const newQueryContainer = document.createElement("div");
    newQueryContainer.className = "queryContainer";
    const newParagraph = document.createElement("p");
    newParagraph.className = "query";
    newParagraph.innerHTML = chatGPTQuestion.value;
    newQueryContainer.appendChild(newParagraph);
    chatGPTResp.appendChild(newQueryContainer);
    chatGPTQuestion.value = "";

}