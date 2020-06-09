$("#questions").hide()
$("#answers").hide()
let correct = []
let gotItRight = []

$("#makeQuiz").on("click", function newQuiz(e) {
    e.preventDefault();
    makeQuiz();
    $("#quizForm").hide();
    $("#questions").show();
});

$("#submitQuiz").on("click", function checkAnswers(e) {
    e.preventDefault()

    const num_questions = $("#quizQuestion").children().length

    for (let i = 0; i < num_questions; i++) {
        const answer = correct[i];
        const selected = $(`input[name=${i}]:checked`).val();

        if (answer.includes(selected)) {
            gotItRight.push(answer)
        }
    }

    for (let i = 0; i < gotItRight.length; i++) {
        $("#correct_answers").append(`
            <li>${gotItRight[i]}</li>
        `)
    }

    $("#numQuestionsForm").val(num_questions)
    $("#categoryForm").val($("#quizTitle").text())
    $("#correctAnswersForm").val(gotItRight.length)

    $("#questions").hide();
    $("#answers").show();
});

async function makeQuiz() {
    const category = $("#category").val()
    const num_questions = $('#num_questions').val()
    const response = await axios.get(`https://opentdb.com/api.php?amount=${num_questions}&category=${category}&type=multiple`)
    const res = response.data.results
    $("#quizTitle").text(res[0].category)

    for (let i = 0; i < res.length; i++) {

        correct.push(res[i].correct_answer)

        const answers = allAnswers(res[i]);        
        const shufAns = shuffle(answers);
        $("#quizQuestion").append(`
            <li>
                <h4>${res[i].question}<h4>
                <div class='mb-5 ${i}'>
                    <div class='row align-items-center'>
                        <input checked type='radio' name=${i} value='${shufAns[0]}'
                        <label class='m-3'  for='${1}'>${shufAns[0]}</label>
                    </div>
                    <div class='row align-items-center'>
                        <input type='radio' name=${i} value='${shufAns[1]}'
                        <label class='m-3 for='${2}'>${shufAns[1]}</label>
                    </div>
                    <div class='row align-items-center'>
                        <input type='radio' name=${i} value='${shufAns[2]}'
                        <label class='m-3 for='${3}'>${shufAns[2]}</label>
                    </div>
                    <div class='row align-items-center'>
                        <input type='radio' name=${i} value='${shufAns[3]}'
                        <label class='m-3 for='${4}'>${shufAns[3]}</label>
                    </div>
                </div>                      
            </li>   
        `)
    }
}


function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr
}

function allAnswers(data) {
    let answers = []
    answers.push(data.correct_answer);
    for (let i = 0; i < data.incorrect_answers.length; i++) {
        answers.push(data.incorrect_answers[i])
    }
    return answers;
}