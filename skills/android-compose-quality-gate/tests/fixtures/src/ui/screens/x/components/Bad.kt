@Composable
fun Bad() {
    Row(Modifier.height(IntrinsicSize.Min).offset(x = 4.dp).padding(paddingLeft = 2.dp)) {
        Text("Hardcoded", color = Color(0xFF112233))
    }
    Log.d("x", "y")
}
