const form =
    document.getElementById(
        "lookup-form"
    );


form.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        const value =
            document
                .getElementById(
                    "indicator"
                )
                .value
                .trim();


        if (!value) {

            return;

        }


        const validationBox =
            document.getElementById(
                "validation-result"
            );


        validationBox.className =
            "validation-box muted";


        validationBox.textContent =
            "Analyzing indicator locally...";


        try {

            const response =
                await fetch(
                    "/api/investigation/lookup?value=" +
                    encodeURIComponent(value)
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Investigation failed."
                );

            }


            renderValidation(
                data.validation
            );


            renderMatches(
                data.matches
            );


        }

        catch (error) {

            validationBox.className =
                "validation-box invalid";


            validationBox.textContent =
                error.message;

        }

    }
);


function renderValidation(
    validation
) {

    const box =
        document.getElementById(
            "validation-result"
        );


    if (validation.valid) {

        box.className =
            "validation-box valid";


        box.innerHTML = `

            <strong>
                VALID INDICATOR
            </strong>

            ·

            Type:
            ${escapeHtml(
                validation.indicator_type
            )}

            ·

            ${escapeHtml(
                validation.validation_notes
            )}

        `;

    }

    else {

        box.className =
            "validation-box invalid";


        box.innerHTML = `

            <strong>
                INVALID INDICATOR
            </strong>

            ·

            ${escapeHtml(
                validation.validation_notes
            )}

        `;

    }

}


function renderMatches(
    matches
) {

    const section =
        document.getElementById(
            "investigation-results"
        );


    const container =
        document.getElementById(
            "matches"
        );


    const count =
        document.getElementById(
            "match-count"
        );


    section.classList.remove(
        "hidden"
    );


    count.textContent =
        matches.length +
        (
            matches.length === 1
                ? " match"
                : " matches"
        );


    if (!matches.length) {

        container.innerHTML = `

            <div class="panel">

                <div class="loading">

                    No matching local threat
                    records were found.

                    <br><br>

                    No external network
                    lookup was performed.

                </div>

            </div>

        `;

        return;

    }


    container.innerHTML =
        matches.map(
            match => {

                let attackHtml = "";


                if (
                    match.attack_mapping
                ) {

                    attackHtml = `

                        <div class="attack-box">

                            <strong>
                                ATT&CK Context
                            </strong>

                            <br>

                            Tactic:
                            ${escapeHtml(
                                match
                                    .attack_mapping
                                    .tactic
                            )}

                            <br>

                            Technique:
                            ${escapeHtml(
                                match
                                    .attack_mapping
                                    .technique_id
                            )}

                            ·

                            ${escapeHtml(
                                match
                                    .attack_mapping
                                    .technique
                            )}

                        </div>

                    `;

                }


                return `

                    <article
                        class="match-card"
                    >

                        <div class="match-top">

                            <h3>

                                ${escapeHtml(
                                    match.name
                                )}

                            </h3>

                            <span class="badge">

                                Risk
                                ${match.risk_score}

                            </span>

                        </div>


                        <p>

                            ${escapeHtml(
                                match.description
                            )}

                        </p>


                        <div class="kv">

                            <div>

                                <span>
                                    Indicator
                                </span>

                                <strong>
                                    ${escapeHtml(
                                        match
                                            .indicator_value
                                    )}
                                </strong>

                            </div>


                            <div>

                                <span>
                                    Category
                                </span>

                                <strong>
                                    ${escapeHtml(
                                        match.category
                                    )}
                                </strong>

                            </div>


                            <div>

                                <span>
                                    Severity
                                </span>

                                <strong>
                                    ${escapeHtml(
                                        match.severity
                                    )}
                                </strong>

                            </div>


                            <div>

                                <span>
                                    Status
                                </span>

                                <strong>
                                    ${escapeHtml(
                                        match.status
                                    )}
                                </strong>

                            </div>

                        </div>


                        ${attackHtml}

                    </article>

                `;

            }
        ).join("");

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