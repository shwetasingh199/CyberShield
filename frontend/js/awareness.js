let quizData = [];


async function loadAwareness() {

    try {

        const responses =
            await Promise.all([

                fetch(
                    "/api/awareness/modules"
                ),

                fetch(
                    "/api/awareness/quiz"
                )

            ]);


        const modules =
            await responses[0].json();


        quizData =
            await responses[1].json();


        renderModules(
            modules
        );


        renderQuiz(
            quizData
        );

    }

    catch (error) {

        console.error(
            "Awareness error:",
            error
        );


        document.getElementById(
            "modules"
        ).innerHTML = `

            <div class="panel">

                <div class="loading">

                    Awareness content could
                    not be loaded.

                    <br><br>

                    Make sure Flask is running.

                </div>

            </div>

        `;

    }

}


function renderModules(
    modules
) {

    const container =
        document.getElementById(
            "modules"
        );


    if (!modules.length) {

        container.innerHTML = `

            <div class="panel">

                <div class="loading">

                    No awareness modules
                    are available yet.

                </div>

            </div>

        `;

        return;

    }


    container.innerHTML =
        modules.map(
            module => `

                <article
                    class="module-card"
                >

                    <span
                        class="module-tag"
                    >

                        ${escapeHtml(
                            module.category
                        )}

                    </span>


                    <h3>

                        ${escapeHtml(
                            module.title
                        )}

                    </h3>


                    <p>

                        ${escapeHtml(
                            module.content
                        )}

                    </p>


                    <div
                        class="module-footer"
                    >

                        <span>

                            ${escapeHtml(
                                module.difficulty
                            )}

                        </span>

                        <span>

                            Defensive Training

                        </span>

                    </div>

                </article>

            `
        ).join("");

}


function renderQuiz(
    questions
) {

    const container =
        document.getElementById(
            "quiz"
        );


    document.getElementById(
        "quiz-progress"
    ).textContent =
        questions.length +
        " questions";


    if (!questions.length) {

        container.innerHTML = `

            <div class="loading">

                No quiz questions available.

            </div>

        `;

        return;

    }


    container.innerHTML =
        questions.map(
            (question, index) => `

                <div
                    class="question"
                >

                    <h3>

                        ${index + 1}.
                        ${escapeHtml(
                            question.question
                        )}

                    </h3>


                    ${question.options.map(
                        (option, optionIndex) => `

                            <label
                                class="option"
                            >

                                <input
                                    type="radio"
                                    name="question-${index}"
                                    value="${optionIndex}"
                                >

                                ${escapeHtml(
                                    option
                                )}

                            </label>

                        `
                    ).join("")}

                </div>

            `
        ).join("");

}


async function submitQuiz() {

    if (!quizData.length) {

        return;

    }


    let score = 0;


    quizData.forEach(
        (question, index) => {

            const selected =
                document.querySelector(
                    `input[name="question-${index}"]:checked`
                );


            if (
                selected &&
                Number(
                    selected.value
                ) === question.answer
            ) {

                score++;

            }

        }
    );


    try {

        const response =
            await fetch(
                "/api/awareness/quiz/submit",
                {
                    method:
                        "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            score:
                                score,

                            total:
                                quizData.length
                        })
                }
            );


        const result =
            await response.json();


        if (!response.ok) {

            throw new Error(
                result.error ||
                "Unable to submit quiz."
            );

        }


        const resultBox =
            document.getElementById(
                "quiz-result"
            );


        resultBox.classList.remove(
            "hidden"
        );


        resultBox.innerHTML = `

            <strong>
                Quiz Result
            </strong>

            <br><br>

            ${result.score}
            /
            ${result.total}
            correct

            ·

            ${result.percentage}%

            <br><br>

            Continue reviewing the modules
            and retake the assessment to
            reinforce the concepts.

        `;

    }

    catch (error) {

        console.error(
            error
        );

        alert(
            error.message
        );

    }

}


function escapeHtml(
    value
) {

    const element =
        document.createElement(
            "div"
        );

    element.textContent =
        value ?? "";

    return element.innerHTML;

}


loadAwareness();