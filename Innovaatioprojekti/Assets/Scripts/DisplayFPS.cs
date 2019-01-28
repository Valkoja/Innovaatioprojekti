using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class DisplayFPS : MonoBehaviour
{
    public bool displayFPS;
    public Text fpsText;

    float deltaTime = 0.0f;

    // Start is called before the first frame update
    void Start()
    {
        displayFPS = true;  
    }

    // Update is called once per frame
    void Update()
    {
        deltaTime += (Time.unscaledDeltaTime - deltaTime) * 0.1f;
    }

    void OnGUI()
    {
        float msec = deltaTime * 1000.0f;
        float fps = 1.0f / deltaTime;
        if (displayFPS)
        {
            fpsText.text = fps.ToString().Substring(0, 4) + " FPS";
        }
        else fpsText.text = "";
    }

    public void ToggleFPSVisibility(bool setValue)
    {
        displayFPS = setValue;
    }
}