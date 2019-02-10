using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UITextEdit : MonoBehaviour
{
    public double xValue;
    public double yValue;
    public double zValue;
    public Text xText;
    public Text yText;
    public Text zText;

    // Start is called before the first frame update
    void Start()
    {
        xValue = 0.0;
        yValue = 0.0;
        zValue = 0.0;
    }

    // Update is called once per frame
    void Update()
    {
        if (xValue == 0.0 && yValue == 0.0 && zValue == 0.0)
        {
            SetTextNoData();
        }
        else SetTextWith(xValue, yValue, zValue);
    }

    void SetTextNoData()
    {
        xText.text = "No Data";
        yText.text = " ";
        zText.text = " ";
    }

    void SetTextWith(double x, double y, double z) {

        xText.text = "X: " + x.ToString();
        yText.text = "Y: " + y.ToString();
        zText.text = "Z: " + z.ToString();
    }
}
