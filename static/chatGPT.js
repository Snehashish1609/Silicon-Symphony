self.addEventListener('message', (event) => {
    const getAnswer = (data) => {
        const words = data.split(" ");
        const salutations = ["hi", "greetings", "hello"];
        const questions = ["what", "where", "when", "who", "how", "?"];
        const pandaquests = ["panda", "pandaquests", "cool", "blog"];
        let isGreeting = false;
        let isAsking = false;
        let isPandaquests = false;
        
        words.forEach(element => {
            const elementSanitized = element.toLowerCase();
            
            if (salutations.includes(elementSanitized)) {
                isGreeting = true;
            }
            if (questions.includes(elementSanitized)) {
                isAsking = true;
            }
            if (pandaquests.includes(elementSanitized)) {
                isPandaquests = true;
            }
        });
    
        if (isPandaquests) {
            const variedAnswers = [
                "test",
                "test2", 
                "test3"
            ]            
            
            return variedAnswers[Math.floor(Math.random() * variedAnswers.length)];
        } else if (isGreeting) {
            return `Oh, hello there. How are you?`;
        } else {
            const url = `/api/v1.0/get-cluster/${encodeURIComponent(data)}`;
            return fetch(url)
                .then(response => response.text())
                .catch(error => {
                    console.error('Error calling API:', error);
                    return "Sorry, I couldn't find an answer to your question.";
                });
        }
        //return "The answer is 42";
    }   
    const { data } = event;
    console.log("received: data", data);
    
    const answer = getAnswer(data);
    if (answer instanceof Promise) {
        answer.then(result => self.postMessage(result));
    } else {
        self.postMessage(answer);
    }
});
