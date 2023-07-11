class Solution {
    public String mergeAlternately(String word1, String word2) {
        int l1 = word1.length();
        int l2 = word2.length();
        int m;
        String n = "";
        String last = "";
        if (l1>l2){
            m = l2;
            last = word1.substring(m,l1);
        }else{
            m = l1;
            last = word2.substring(m,l2);
        }
        for (int i = 0; i<m;i++){
            n=n+word1.charAt(i);
            n=n+word2.charAt(i);
        }
        n+=last;
        return n;
        
    }
}