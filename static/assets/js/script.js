function ready(fn) {
  if (document.readyState != 'loading') {
    fn();
  } else {
    document.addEventListener('DOMContentLoaded', fn);
  }
}

ready(choices);

var content =
[
  {question: 'How many months have 28 days?', choices: [1, 6, 8, 12], correct: 3},
  {question: 'What is the missing number: 4, 8, 14, 22, ?', choices: [26, 28, 32, 36], correct: 2},
  {question: 'There are 12 pens on the table, you took 3, how many do you have?', choices: [3, 12, 9, 15], correct: 0},
  {question: 'Solve this equation using an algebraic method: (x + 4)( x - 4) = 9', choices: ['x = 5', 'x = 5 and x = -5', 'x = 9', 'x = 4 and x= -4'], correct: 1},
  {question: 'Which of the words below is spelled incorrectly?', choices: ['Inoculate', 'Consensus', 'Liquefy', 'Sacreligious'], correct: 3},
];

var x = 0;
var y = 1;
var score = 0;

function choices() {
  if (content[x] === undefined) {
    document.querySelector('.score').textContent = 'Score: ' + score;
    document.form1.style.visibility = 'hidden';
    document.querySelector('.header').style.visibility = 'hidden';

  } else {
    var questionNumber = document.querySelector('.questionNumber');
    questionNumber.textContent = 'Question#' + y;

    var question = document.querySelector('.question');
    question.textContent = content[x]['question'];

    var choices = document.querySelectorAll('label');
    for (var i = 0; i < choices.length; i++) {
      choices[i].textContent = content[x]['choices'][i];
    }
  }
}

function next() {
  var inputs = document.querySelectorAll('input');

  if (content[x] === undefined) {
    return false;
  }

  else if (inputs[0].checked !== true && inputs[1].checked !== true && inputs[2].checked !== true && inputs[3].checked !== true) {
    alert('Please select an answer');

  } else {
    for (var i = 0; i < inputs.length; i++) {
      if (inputs[i].checked === true && i === content[x]['correct']) {
        score++;
      }
    inputs[i].checked = false;
  }

  x++;
  y++;
  choices();
  }
}

function back() {
  var inputs = document.querySelectorAll('input');

  if (x === 0) {
    return false;

  } else {
    x--;
    y--;
    choices();
  }
}