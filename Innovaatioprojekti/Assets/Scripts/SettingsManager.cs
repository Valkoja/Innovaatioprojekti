using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Events;

public class SettingsManager : MonoBehaviour
{
    public Slider consoleSizeSlider;
    public Text consoleTextT;
    public Text consoleTextR;
    public Text consoleTextL;
    public Text consoleSizeText;

    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        consoleTextL.fontSize = consoleTextR.fontSize = consoleTextT.fontSize = (int)consoleSizeSlider.value;
        consoleSizeText.text = "Console text size (" + consoleSizeSlider.value.ToString()+")";
    }
    
}
