async function loadDashboard() {

    try {

        const response =
            await fetch(
                "/api/dashboard/stats"
            );

        if (!response.ok) {

            throw new Error(
                "Dashboard API returned " +
                response.status
            );

        }

        const data =
            await response.json();


        setText(
            "total-threats",
            data.total_threats
        );

        setText(
            "active-alerts",
            data.active_alerts
        );

        setText(
            "high-risk",
            data.high_risk_threats
        );

        setText(
            "critical-vulns",
            data.critical_vulnerabilities
        );

        setText(
            "investigations",
            data.investigations
        );


        renderSeverity(
            data.threat_severity || {}
        );


        renderCategories(
            data.categories || []
        );


        renderThreats(
            data.recent_threats || []
        );


        renderAlerts(
            data.recent_alerts || []
        );


    }

    catch (error) {

        console.error(
            "Dashboard error:",
            error
        );

        showToast(
            "Unable to load dashboard data."
        );

    }

}


function setText(
    id,
    value
) {

    const element =
        document.getElementById(id);

    if (element) {

        element.textContent =
            value;

    }

}


function renderSeverity(
    data
) {

    const container =
        document.getElementById(
            "severity-bars"
        );


    const order = [

        "CRITICAL",
        "HIGH",
        "MEDIUM",
        "LOW",
        "INFORMATIONAL"

    ];


    const values =
        order.map(
            level =>
                data[level] || 0
        );


    const maximum =
        Math.max(
            1,
            ...values
        );


    container.innerHTML =
        order.map(
            level => {

                const value =
                    data[level] || 0;

                const percentage =
                    (
                        value /
                        maximum
                    ) * 100;


                return `

                    <div class="bar-row">

                        <span>
                            ${level}
                        </span>

                        <div class="bar-track">

                            <div
                                class="bar-fill"
                                style="
                                    width:${percentage}%;
                                "
                            ></div>

                        </div>

                        <strong>
                            ${value}
                        </strong>

                    </div>

                `;

            }
        ).join("");

}


function renderCategories(
    categories
) {

    const container =
        document.getElementById(
            "category-list"
        );


    if (!categories.length) {

        container.innerHTML = `
            <div class="loading">
                No category data available.
            </div>
        `;

        return;

    }


    container.innerHTML =
        categories.map(
            item => `

                <div class="category-item">

                    <span>
                        ${escapeHtml(
                            item.category
                        )}
                    </span>

                    <span>
                        ${item.count}
                    </span>

                </div>

            `
        ).join("");

}


function renderThreats(
    threats
) {

    const table =
        document.getElementById(
            "threat-table"
        );


    if (!threats.length) {

        table.innerHTML = `

            <tr>

                <td
                    colspan="5"
                    class="loading"
                >
                    No threat records available.
                </td>

            </tr>

        `;

        return;

    }


    table.innerHTML =
        threats.map(
            threat => `

                <tr>

                    <td>
                        ${escapeHtml(
                            threat.name
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            threat.category
                        )}
                    </td>

                    <td>
                        ${escapeHtml(
                            threat.severity
                        )}
                    </td>

                    <td>

                        <span class="badge">

                            ${threat.risk_score}

                        </span>

                    </td>

                    <td>

                        <span class="status-chip">

                            ${escapeHtml(
                                threat.status
                            )}

                        </span>

                    </td>

                </tr>

            `
        ).join("");

}


function renderAlerts(
    alerts
) {

    const container =
        document.getElementById(
            "alert-list"
        );


    if (!alerts.length) {

        container.innerHTML = `

            <div class="loading">

                No alert records available.

            </div>

        `;

        return;

    }


    container.innerHTML =
        alerts.map(
            alert => `

                <div class="alert-item">

                    <strong>

                        ${escapeHtml(
                            alert.title
                        )}

                    </strong>

                    <small>

                        Threat:
                        ${escapeHtml(
                            alert.threat_name ||
                            "Unknown"
                        )}

                    </small>

                    <small>

                        Risk:
                        ${alert.risk_score ?? "N/A"}

                        ·

                        Status:
                        ${escapeHtml(
                            alert.status
                        )}

                    </small>

                </div>

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


function showToast(
    message
) {

    const toast =
        document.getElementById(
            "toast"
        );


    toast.textContent =
        message;


    toast.classList.add(
        "show"
    );


    setTimeout(
        () => {

            toast.classList.remove(
                "show"
            );

        },
        3000
    );

}


loadDashboard();