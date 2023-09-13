#include <bits/stdc++.h>
using namespace std;
struct node
{
    int data;
    int val ;
    node(int x, int y)
    {
        data = x;
        val = y;
    }
    
    };
    int main(){
        int  n ;
    vector<node> v;
    cin >> n ;
    while (n--)
    {
        int x , y ;
        cin >> x >> y ;
        node temp(x,y);
        v.push_back(temp);
    }
    for (int i = 0; i < v.size(); i++)
    {
        cout << v[i].data << " " << v[i].val << endl;
    }
    return 0;
    }
