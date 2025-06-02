import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

void main() {
  runApp(const LinesOfActionApp());
}

class LinesOfActionApp extends StatelessWidget {
  const LinesOfActionApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Lines of Action',
      theme: ThemeData.dark(),
      home: const GameScreen(),
    );
  }
}

class GameScreen extends StatefulWidget {
  const GameScreen({super.key});

  @override
  State<GameScreen> createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen> {
  List<List<int>> board = List.generate(8, (_) => List.filled(8, 0));

  // Example initial positions: black on top/bottom row, white on left/right columns
  @override
  void initState() {
    super.initState();
    for (int i = 0; i < 8; i++) {
      board[0][i] = 1;
      board[7][i] = 1;
      board[i][0] = -1;
      board[i][7] = -1;
    }
  }

  Future<void> getAIMove() async {
    final url =
        Uri.parse('http://localhost:5000/move'); // Change if hosted elsewhere
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'board': board}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final move = data['move']; // [from_x, from_y, to_x, to_y]

      setState(() {
        int fromX = move[0], fromY = move[1], toX = move[2], toY = move[3];
        int piece = board[fromX][fromY];
        board[fromX][fromY] = 0;
        board[toX][toY] = piece;
      });
    } else {
      print('AI error: ${response.body}');
    }
  }

  Widget buildSquare(int x, int y) {
    int val = board[x][y];
    Color color;
    if (val == 1)
      color = Colors.black;
    else if (val == -1)
      color = Colors.white;
    else
      color = Colors.grey.shade300;

    return GestureDetector(
      onTap: () {
        // For now: just print location tapped
        print('Tapped ($x, $y)');
      },
      child: Container(
        margin: const EdgeInsets.all(1),
        decoration: BoxDecoration(
          color: color,
          border: Border.all(color: Colors.black),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Lines of Action')),
      body: Column(
        children: [
          AspectRatio(
            aspectRatio: 1,
            child: GridView.builder(
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 8,
              ),
              itemCount: 64,
              itemBuilder: (context, index) {
                int x = index ~/ 8;
                int y = index % 8;
                return buildSquare(x, y);
              },
            ),
          ),
          ElevatedButton(
            onPressed: getAIMove,
            child: const Text('Let AI Move'),
          )
        ],
      ),
    );
  }
}
