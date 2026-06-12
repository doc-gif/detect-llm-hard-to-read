public class Example {
    public double calculateDistance(double x, double y) {
        double sum = x * x + y * y;
        if (sum > 0) {
            return Math.sqrt(sum);
        }
        return 0.0;
    }
}