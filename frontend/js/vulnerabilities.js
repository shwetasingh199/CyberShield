async function loadVulnerabilities() {

    try {

        /*
         * Load summary
         */

        const summaryResponse =
            await fetch(
                "/api/vulnerabilities/summary"
            );


        const summary =
            await summaryResponse.json();


        document.getElementById(
            "v-total"
        ).textContent =
            summary.total;


        document.getElementById(
            "v-open"
        ).textContent =
            summary.open;


        document.getElementById(
            "v-critical"
        ).textContent =
            (
                summary
                    .by_severity
                    ?.CRITICAL ||
                0
            );


        document.getElementById(
            "v-evidence"
        ).textContent =
            summary.exploitation_evidence;


        /*
         * Filters
         */

        const severity =
            document
                .getElementById(
                    "severity-filter"
                )
                .value;


        const status =
            document
                .getElementById(
                    "status-filter"
                )
                .value;


        const params =
            new URLSearchParams();


        if (severity) {

            params.set(
                "severity",
                severity
            );

        }


        if (status) {

            params.set(
                "status",
                status
            );

        }


        /*
         * Load vulnerabilities
         */

        const response =
            await fetch(
                "/api/vulnerabilities?" +
                params.toString()
            );


        const vulnerabilities =
            await response.json();


        renderVulnerabilities(
            vulnerabilities
        );

    }

    catch (error) {

        console.error(
            "Vulnerability error:",
            error
        );


        document.getElementById(
            "vuln-table"
        ).innerHTML = `

            <tr>

                <td
                    colspan="8"
                    class="loading"
                >

                    Unable to load vulnerability
                    data.

                    <br><br>

                    Check that Flask is running.

                </td>

            </tr>

        `;

    }

}


function renderVulnerabilities(
    vulnerabilities
) {

    const table =
        document.getElementById(
            "vuln-table"
        );


    if (!vulnerabilities.length) {

        table.innerHTML = `

            <tr>

                <td
                    colspan="8"
                    class="loading"
                >

                    No vulnerabilities match
                    the selected filters.

                </td>

            </tr>

        `;

        return;

    }


    table.innerHTML =
        vulnerabilities.map(
            vulnerability => `

                <tr>

                    <td>

                        <strong>

                            ${escapeHtml(
                                vulnerability.cve_id
                            )}

                        </strong>

                    </td>


                    <td>

                        ${escapeHtml(
                            vulnerability.title
                        )}

                    </td>


                    <td>

                        ${escapeHtml(
                            vulnerability.severity
                        )}

                    </td>


                    <td>

                        <span class="badge">

                            ${vulnerability.cvss}

                        </span>

                    </td>


                    <td>

                        ${vulnerability
                            .asset_criticality
                        }/100

                    </td>


                    <td>

                        ${vulnerability.exposure
                        }/100

                    </td>


                    <td>

                        <span class="status-chip">

                            ${escapeHtml(
                                vulnerability.status
                            )}

                        </span>

                    </td>


                    <td>

                        ${escapeHtml(
                            vulnerability.remediation
                        )}

                    </td>

                </tr>

            `
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


document
    .getElementById(
        "severity-filter"
    )
    .addEventListener(
        "change",
        loadVulnerabilities
    );


document
    .getElementById(
        "status-filter"
    )
    .addEventListener(
        "change",
        loadVulnerabilities
    );


loadVulnerabilities();