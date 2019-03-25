using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ConsoleHandler : Singleton<ConsoleHandler>
{
    protected ConsoleHandler() { }

    List<ListItem> consoleListR = new List<ListItem>(); // bottom right console list
    List<ListItem> consoleListT = new List<ListItem>(); // top left console list
    List<ListItem> consoleListL = new List<ListItem>(); // bottom left console list

    List<string> writeBufferR = new List<string>();
    List<string> writeBufferT = new List<string>();
    List<string> writeBufferL = new List<string>();
    int countR = 0;
    int countT = 0;
    int countL = 0;

    public Text consoleTextR;
    public Text consoleTextT;
    public Text consoleTextL;

    // Start is called before the first frame update
    void Start()
    {
        consoleTextR.text = consoleTextT.text = consoleTextL.text = "";
    }

    // Update is called once per frame
    void Update()
    {
        Print();
    }

    void Print()
    {
        consoleTextR.text = consoleTextT.text = consoleTextL.text = "";
        WriteMsg();
        WriteData();
        for (int i = 0; i < writeBufferR.Count; i++)
        {
            consoleTextR.text += writeBufferR[i] + "\n";
        }
        for (int i = 0; i < writeBufferT.Count; i++)
        {
            consoleTextT.text += writeBufferT[i] + "\n";
        }
        for (int i = 0; i < writeBufferL.Count; i++)
        {
            consoleTextL.text += writeBufferL[i] + "\n";
        }
        writeBufferT.Clear();
        writeBufferL.Clear();
        writeBufferR.Clear();
    }

    void WriteData()
    {
        for (int i = 0; i < countR; i++)
        {
            if (consoleListR[i].GetAType() == 0)
            {
                writeBufferR.Add(consoleListR[i].GetData());
            }
        }
        for (int i = 0; i < countT; i++)
        {
            if (consoleListT[i].GetAType() == 0)
            {
                writeBufferT.Add(consoleListT[i].GetData());
            }
        }
        for (int i = 0; i < countL; i++)
        {
            if (consoleListL[i].GetAType() == 0)
            {
                writeBufferL.Add(consoleListL[i].GetData());
            }
        }
    }

    void WriteMsg()
    {
        for (int i = 0; i < countR; i++)
        {
            if (writeBufferR.Count <= 10 && consoleListR[i].GetAType() == 1)
            {
                writeBufferR.Add(consoleListR[i].GetData());
            }
            else if (writeBufferR.Count > 10 && consoleListR[i].GetAType() == 1)
            {
                RemoveOldestMsg("R");
                countR--;
            }
        }
        for (int i = 0; i < countL; i++)
        {
            if (writeBufferL.Count <= 10 && consoleListL[i].GetAType() == 1)
            {
                writeBufferL.Add(consoleListL[i].GetData());
            }
            else if (writeBufferL.Count > 10 && consoleListL[i].GetAType() == 1)
            {
                RemoveOldestMsg("L");
                countL--;
            }
        }
        for (int i = 0; i < countT; i++)
        {
            if (writeBufferT.Count <= 10 && consoleListT[i].GetAType() == 1)
            {
                writeBufferT.Add(consoleListT[i].GetData());
            }
            else if (writeBufferT.Count > 10 && consoleListT[i].GetAType() == 1)
            {
                RemoveOldestMsg("T");
                countT--;
            }
        }
    }

    void RemoveOldestMsg(string location)
    {
        if (location == "R")
            for (int i = 0; i < countR; i++)
            {
                if (consoleListR[i].GetAType() == 1)
                {
                    consoleListR.RemoveAt(i);
                    return;
                }
            }
        else if (location == "T")
            for (int i = 0; i < countT; i++)
            {
                if (consoleListT[i].GetAType() == 1)
                {
                    consoleListT.RemoveAt(i);
                    return;
                }
            }
        else if (location == "L")
            for (int i = 0; i < countL; i++)
            {
                if (consoleListL[i].GetAType() == 1)
                {
                    consoleListL.RemoveAt(i);
                    return;
                }
            }
    }

    public void AddItemToConsole(ListItem item)
    {
        if (item.GetLocation() == "R")
        {
            consoleListR.Add(item);
            countR++;
        }
        else if (item.GetLocation() == "L")
        {
            consoleListL.Add(item);
            countL++;
        }
        else if (item.GetLocation() == "T")
        {
            consoleListT.Add(item);
            countT++;
        }
        else
        {
            Debug.Log("Location not found: " + item.GetLocation());
        }
    }

    public void RemoveItemFromConsole(ListItem item, string location)
    {
        
        if (location == "R")
        {
            consoleListR.Remove(item);
            countR--;
        }
        else if (location == "L")
        {
            consoleListL.Remove(item);
            countL--;
        }
        else if (location == "T")
        {
            consoleListT.Remove(item);
            countT--;
        }
        else
        {
            Debug.Log("Location not found: " + location);
        }
        
    }
}

public class ListItem
{
    int atype;
    string data = "";
    string alocation = "";
    public ListItem(int type/* 0 = data, 1 = msg, 2 = hidden */, string location/*R = bottom right, L = bottom left, T = top left*/)
    {
        atype = type;
        alocation = location;
    }
    public ListItem(string text,int type/* 0 = data, 1 = msg, 2 = hidden */, string location/*R = bottom right, L = bottom left, T = top left*/)
    {
        atype = type;
        data = text;
        alocation = location;
    }
    
    public string GetLocation()
    {
        return alocation;
    }

    public void SetData(string s)
    {
        data = s;
    }

    public void SetAType(int type)
    {
        atype = type;
    }

    public int GetAType()
    {
        return atype;
    }

    public string GetData()
    {
        return data;
    }
}
