using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class IPSetHandler : MonoBehaviour
{
    public Text inputFieldText;
    public Text currentHostIPText;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void OnPressConfirm()
    {
        if (IsInputIPCorrect(inputFieldText.text))
        {
            currentHostIPText.text = inputFieldText.text;
        }
    }

    public void OnPressCancel()
    {
        // tanne jtn?
    }

    bool IsInputIPCorrect(string input)
    {
        if (input != "")
        {
            return true;
        }
        else return false;
    }
}
