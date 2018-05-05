import java.io.*;

public class Fifth {
    public static void main(String[] args) {
        while(true) {
            System.out.print("Enter a word: ");

            BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

            String word = null;

            try {
                word = br.readLine();
            } catch(IOException ioe) {
                System.out.println("IO error trying to read your word!");
                System.exit(1);
            }

            char last = word.charAt(0);
            System.out.print(last);
            for(int i = 1; i < word.length(); i++) {
                char l = word.charAt(i);
                if(last == l) {
                    System.out.print('a');
                }
                System.out.print(l);
                last = l;
            }
            System.out.println();
        }
    }

}
