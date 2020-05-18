var name = "";

var app = new Vue({
  el: '#game',
  data: {
    board: [
      ['', '', ''],
      ['', '', ''],
      ['', '', ''],
    ],
    is_over: false,
    current_player: 0,
    // nick: "",
    players: ['X', 'O'],
    message: 'Ход X',
    is_win: 0,
    you: ""
  },
  methods: {
    tap: function(e) {
      let i = e.target.attributes['data-row'].value;
      let j = e.target.attributes['data-column'].value;
      send_click(i, j)
      get_state()

      return 0;
    },
  }
})


function get_state() {
    $.get("/get_state", function(data) {
        app.board = data["field"];
        app.is_win = data["is_win"]
        app.you = data["you"]
        app.message = 'Ход ' + data["player"]

        if (app.is_win || app.board.flat().every((x) => x != '')) {
            app.is_over = true;
            if (app.is_win > 0) {
                app.message = 'Кресты победили'
            } else if (app.is_win < 0) {
                app.message = 'Нолики победили'
            } else {
                app.message = 'Ну ничья и ничья'
            }
        }

        if (data["ready"] == false) {
            app.message = 'Нужны игроки'
            console.log(app.message)
        }
    });
};

get_state();
setInterval(get_state, 500);


function send_click(i, j) {
    $.ajax("/click", {
        data : JSON.stringify({
            // "player": name,
            "i": i,
            "j": j,
        }),
        contentType : 'application/json',
        type : 'POST',
    }, );
};
