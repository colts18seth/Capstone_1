$("#questions").hide()

$("#makeQuiz").on("click", async function makeQuiz(e) {
    e.preventDefault();
    $("#quizForm").hide();
    const category = $( "#category" ).val()
    const num_questions = $('#num_questions').val()
    const response = await axios.get(`https://opentdb.com/api.php?amount=${num_questions}&category=${category}&type=multiple`)
    res = response.data.results
    $("#quizTitle").text(res[0].category)

    for(let i = 0; i < res.length; i++){
        const answers = allAnswers(res[i]);
        const shufAns = shuffle(answers);
        $("#quizQuestion").append(`
            <li>
                <h4>${res[i].question}<h4>
                <div class='mb-5'>
                    <input type='radio' id='${1}' name=${res[i].question} value=${shufAns[0]}
                    <label class='ml-3' for='${1}'> ${shufAns[0]}</label>
                    <input type='radio' id='${2}' name=${res[i].question} value=${shufAns[1]}
                    <label class='ml-3' for='${2}'> ${shufAns[1]}</label>
                    <input type='radio' id='${3}' name=${res[i].question} value=${shufAns[2]}
                    <label class='ml-3' for='${3}'> ${shufAns[2]}</label>
                    <input type='radio' id='${4}' name=${res[i].question} value=${shufAns[3]}
                    <label class='ml-3' for='${4}'> ${shufAns[3]}</label>
                </div>                      
            </li>   
        `)
    }
    
    
    
    $("#questions").show();
    
    function makeQuestion(data){
        let answers = allAnswers(data)
        

    }

    function shuffle(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr
    }
    
    function allAnswers(data){
        let answers = []
        answers.push(data.correct_answer);
        for(let i = 0; i < data.incorrect_answers.length; i++){
            answers.push(data.incorrect_answers[i])
        }        
        return answers;
    }
});