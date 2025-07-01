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
  late List<List<int>> board;
  Offset? tapStart;
  bool isLoading = false; // Add a loading state

  @override
  void initState() {
    super.initState();
    board = initializeBoard();
  }

  List<List<int>> initializeBoard() {
    List<List<int>> newBoard = List.generate(8, (_) => List.filled(8, 0));
    for (int i = 1; i < 7; i++) {
      newBoard[0][i] = 1;
      newBoard[7][i] = 1;
      newBoard[i][0] = -1;
      newBoard[i][7] = -1;
    }
    return newBoard;
  }

  Future<void> getAIMove() async {
    setState(() {
      isLoading = true; // Set loading to true
    });

    final url = Uri.parse('http://127.0.0.1:5050/move'); // Change if hosted elsewhere
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'board': board}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      final move = data['move']; // [from_x, from_y, to_x, to_y]

      setState(() {
        applyMove(move[0][0], move[0][1], move[1][0], move[1][1]);
        isLoading = false; // Set loading to false
      });
    } else {
      setState(() {
        isLoading = false; // Set loading to false even on error
      });
      print('AI error: ${response.body}');
    }
  }

  void applyMove(int fromX, int fromY, int toX, int toY) {
    int piece = board[fromX][fromY];
    board[fromX][fromY] = 0;
    board[toX][toY] = piece;
  }

  void registerHumanMove(int fromX, int fromY, int toX, int toY) {
    setState(() {
      applyMove(fromX, fromY, toX, toY);
    });
  }

  Offset calculateGridPosition(RenderBox box, Offset globalPosition) {
    Offset localPosition = box.globalToLocal(globalPosition);
    double squareSize = box.size.width / 8;
    int x = (localPosition.dy / squareSize).floor() - 2;
    int y = (localPosition.dx / squareSize).floor();
    return Offset(x.toDouble(), y.toDouble());
  }

  Widget buildSquare(int x, int y) {
    int val = board[x][y];
    Color color;
    if (val == 1) {
      color = Colors.black;
    } else if (val == -1) {
      color = Colors.white;
    } else {
      color = const Color.fromARGB(255, 161, 142, 127);
    }

    Offset? tapStart;
    Offset? lastKnownPosition;

    return GestureDetector(
      onTapDown: (details) {
        // Capture the initial touch position immediately
        RenderBox box = context.findRenderObject() as RenderBox;
        tapStart = calculateGridPosition(box, details.globalPosition);
        lastKnownPosition =
            details.globalPosition; // Store the starting position
      },
      onPanStart: (details) {
        // Optionally, update the starting position if needed
        RenderBox box = context.findRenderObject() as RenderBox;
        tapStart ??= calculateGridPosition(box, details.globalPosition);
        lastKnownPosition = details.globalPosition;
      },
      onPanUpdate: (details) {
        // Update the last known position during the drag
        lastKnownPosition = details.globalPosition;
      },
      onPanEnd: (details) {
        // Handle the end of a drag or tap
        if (tapStart != null && lastKnownPosition != null) {
          RenderBox box = context.findRenderObject() as RenderBox;
          Offset tapEnd = calculateGridPosition(
              box, lastKnownPosition!); // Use the last known position

          int fromX = tapStart!.dx.toInt();
          int fromY = tapStart!.dy.toInt();
          int toX = tapEnd.dx.toInt();
          int toY = tapEnd.dy.toInt();

          if (board[fromX][fromY] != 0) {
            registerHumanMove(fromX, fromY, toX, toY);
          }
        }
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
      body: GestureDetector(
        onPanUpdate: (_) {}, // Intercept gestures to prevent scrolling
        child: Column(
          children: [
            AspectRatio(
              aspectRatio: 1,
              child: GridView.builder(
                physics: const NeverScrollableScrollPhysics(), // Disable scrolling
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
              onPressed: isLoading ? null : getAIMove, // Disable button when loading
              child: isLoading
                  ? const CircularProgressIndicator() // Show loading indicator
                  : const Text('Let AI Move'),
            ),
            if (!isLoading) const Text('AI Move Completed'), // Show status
          ],
        ),
      ),
    );
  }
}
