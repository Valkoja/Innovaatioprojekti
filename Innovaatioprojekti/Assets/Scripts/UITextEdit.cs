using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UITextEdit : MonoBehaviour
{
    public double xValue;
    public double yValue;

    public Text xText;
    public Text yText;

    // Start is called before the first frame update
    void Start()
    {
        xValue = 0.0;
        yValue = 0.0;
        SetTextWith(xValue, yValue);
    }

    // Update is called once per frame
    void Update()
    {
        SetTextWith(xValue, yValue);
    }

    void SetTextWith(double x, double y) {
        xText.text = "X: "+x.ToString();
        yText.text = "Y: "+y.ToString();
    }
}
