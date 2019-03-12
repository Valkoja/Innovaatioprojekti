using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ConsoleHandlerT : Singleton<ConsoleHandlerT>
{
    protected ConsoleHandlerT() { }

    List<ListItemT> consoleList = new List<ListItemT>();
    List<string> writeBuffer = new List<string>();
    int count = 0;

    public Text consoleTextTop;

    // Start is called before the first frame update
    void Start()
    {
        consoleTextTop.text = "";
    }

    // Update is called once per frame
    void Update()
    {
        Print();
    }

    void Print()
    {
        consoleTextTop.text = "";
        WriteMsg();
        WriteData();
        for (int i = 0; i < writeBuffer.Count; i++)
        {
            consoleTextTop.text += writeBuffer[i] + "\n";
        }
        writeBuffer.Clear();
    }

    void WriteData()
    {
        for (int i = 0; i < count; i++)
        {
            if (consoleList[i].GetAType() == 0)
            {
                writeBuffer.Add(consoleList[i].GetData());
            }
        }
    }

    void WriteMsg()
    {
        for (int i = 0; i < count; i++)
        {
            if (writeBuffer.Count <= 10 && consoleList[i].GetAType() == 1)
            {
                writeBuffer.Add(consoleList[i].GetData());
            }
            else if (writeBuffer.Count > 10 && consoleList[i].GetAType() == 1)
            {
                RemoveOldestMsg();
                count--;
            }
        }
    }

    void RemoveOldestMsg()
    {
        for (int i = 0; i < count; i++)
        {
            if (consoleList[i].GetAType() == 1)
            {
                consoleList.RemoveAt(i);
                return;
            }
        }
    }

    public void AddItemToConsole(ListItemT item)
    {
        consoleList.Add(item);
        count++;
    }

    public void RemoveItemFromConsole(ListItemT item)
    {
        consoleList.Remove(item);
        count--;
    }
}

public class ListItemT
{
    int atype;
    string data = "";
    public ListItemT(int type/* 0 = data, 1 = msg */)
    {
        atype = type;
    }
    public ListItemT(string text, int type/* 0 = data, 1 = msg */)
    {
        atype = type;
        data = text;
    }

    public void SetData(string s)
    {
        data = s;
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
