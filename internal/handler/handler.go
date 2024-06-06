package handler

import (
	"fmt"
	"net/http"

	"github.com/chasefleming/elem-go"
	"github.com/chasefleming/elem-go/attrs"
	"github.com/chasefleming/elem-go/htmx"
)

func RepoHandler(w http.ResponseWriter, r *http.Request) {

}

func RouteHandler(w http.ResponseWriter, r *http.Request) {

}

func CreationHandler(w http.ResponseWriter, r *http.Request) {

}

func HomeHandler(w http.ResponseWriter, r *http.Request) {
	css := `
        body {
            background-color: #f4f4f4;
            font-family: Arial, sans-serif;
			font-size: 20px;
            height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .button {
            width: 400px;
            height: 70px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 10px 20px;
            background-color: #F5F5F5;
            color: black;
            border: 2px solid #202020;
            margin: 10px;
            cursor: pointer;
            text-align: center;
            text-decoration: none;
			box-shadow: 5px 5px #505050;
			font-size: 20px;
			font-weight: bold;
        }
        .button:hover {
			border: 3px solid #202020;
			box-shadow: 5px 5px #202020;
        }
		footer {
            width: 100%;
            height: 70px;
            background-color: #333;
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            position: fixed;
            bottom: 0;
            left: 0;
        }
		.github-icon {
            fill: #D8D8D8;
			margin-top: 10px;
            margin-left: 10px;
        }
		.github-icon:hover {
			fill: #fff;
		}
    `

	head := elem.Head(nil,
		elem.Script(attrs.Props{attrs.Src: "https://unpkg.com/htmx.org@1.9.6"}),
		elem.Style(nil, elem.Text(css)),
	)

	body := elem.Body(nil,
		elem.H2(nil, elem.Text("Bem-vindo ao portal OpenBoard")),
		elem.Br(nil),
		elem.Br(nil),
		elem.Button(attrs.Props{
			htmx.HXPost: "/repo",
			attrs.Class: "button",
		}, elem.Text("Repositorio de rotas")),
		elem.Button(attrs.Props{
			htmx.HXPost: "/creation",
			attrs.Class: "button",
		}, elem.Text("Criar uma rota")),
		elem.Footer(nil,
			elem.A(attrs.Props{attrs.Href: "https://github.com/tales-hein/OpenBoard", attrs.Target: "_blank"},
				elem.Raw(`<svg class="github-icon" xmlns="http://www.w3.org/2000/svg" width="45px" height="45px" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>`),
			),
		),
	)

	pageContent := elem.Html(nil, head, body)

	html := pageContent.Render()

	w.Header().Set("Content-Type", "text/html")
	_, err := w.Write([]byte(html))
	if err != nil {
		fmt.Printf("Error writing response: %v\n", err)
	}
}
