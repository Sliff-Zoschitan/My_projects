using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp4
{
    public partial class Form1 : Form
    {
        float q = 200;
        float a1 = 0.24f;
        float a2 = 0.1f;
        float a3 = 0.002f;
        float E = 3.0f * Convert.ToSingle(Math.Pow(10, 10));
        float u = 0.22f;
        float[,] f;
        float[,] f1;
        int nf;
        int nf1;
        float r, g, b;
        public void ConvColor(float c)
        {
            if (c < 255)
            {
                r = 0;
                g = c;
                b = 255;
            }
            if (c > 256 && c < 512)
            {
                r = 0;
                g = 255;
                b = 512 - c;
            }
            if (c > 512 && c < 767)
            {
                r = c - 512;
                g = 255;
                b = 0;
            }
            if (c > 768 && c < 1025)
            {
                r = 255;
                g = 1024 - c;
                b = 0;
            }
            if (r > 255) r = 255;
            if (g > 255) g = 255;
            if (b > 255) b = 255;
            if (r < 0) r = 0;
            if (g < 0) g = 0;
            if (b < 0) b = 0;
        }
        public void Raschet()
        {
            float D = (E * a3 * a3 * a3) / (12 * (1 - u * u));
            float dx = a1 / 100.0f;
            float dy = a2 / 100.0f; ;
            float dx1 = a1 / 10.0f;
            float dy1 = a2 / 10.0f;
            nf1 = Convert.ToInt32(a1 / dx1) + 4;
            nf = Convert.ToInt32(a1 / dx) + 4;

            f = new float[nf, nf];
            f1 = new float[nf, nf];
            for (int i = 0; i < nf; i++)
            {
                for (int j = 0; j < nf; j++)
                {
                    f[i, j] = 0;
                }
            }
            //////////////////////////////////////////////////////////////////////////////////////////////////////////
            float fmax = 0;
            for (int it = 0; it < 1000; it++)
            {
                for (int i = 2; i < nf1 - 2; i++)
                {
                    for (int j = 2; j < nf1 - 2; j++)
                    {
                        f1[i, j] = ((dx1 * dx1 * dy1 * dy1 * q) / D + 8 * (f1[i - 1, j] + f1[i + 1, j] + f1[i, j - 1] + f1[i, j + 1]) - 2 * (f1[i - 1, j - 1] + f1[i + 1, j + 1] + f1[i + 1, j - 1] + f1[i - 1, j + 1]) - (f1[i - 2, j] + f1[i + 2, j] + f1[i, j - 2] + f1[i, j + 2])) / 20;
                        if (f1[i, j] > fmax) fmax = f1[i, j];
                    }
                }
            }
            //////////////////////////////////////////////////////////////////////////////////////////////////////////
            float fpr = fmax;
            for (int i = 2; i < nf / 2; i++)
            {
                for (int j = i; j < nf / 2; j++)
                {
                    f[i, j] = (fpr / ((nf - 4) / 2)) * (i - 2);
                    f[j, i] = (fpr / ((nf - 4) / 2)) * (i - 2);
                    f[i, nf - j - 1] = (fpr / ((nf - 4) / 2)) * (i - 2);
                    f[nf - j - 1, i] = (fpr / ((nf - 4) / 2)) * (i - 2);

                    f[nf - i - 1, j] = (fpr / ((nf - 4) / 2)) * (i - 2);
                    f[j, nf - i - 1] = (fpr / ((nf - 4) / 2)) * (i - 2);
                    f[nf - i - 1, nf - j - 1] = (fpr / ((nf - 4) / 2)) * (i - 2);
                    f[nf - j - 1, nf - i - 1] = (fpr / ((nf - 4) / 2)) * (i - 2);
                }
            }
            int nit = 10000;
            for (int it = 0; it < nit; it++)
            {
                for (int i = 2; i < nf - 2; i++)
                {
                    for (int j = 2; j < nf - 2; j++)
                    {
                        f[i, j] = ((dx * dx * dy * dy * q) / D + 8 * (f[i - 1, j] + f[i + 1, j] + f[i, j - 1] + f[i, j + 1]) - 2 * (f[i - 1, j - 1] + f[i + 1, j + 1] + f[i + 1, j - 1] + f[i - 1, j + 1]) - (f[i - 2, j] + f[i + 2, j] + f[i, j - 2] + f[i, j + 2])) / 20;
                    }
                }
            }
        }
        public Form1()
        {
            InitializeComponent();
        }
        private void Draw()
        {
            pictureBox1.Image = null;
            Raschet();
            float min = f[2, 2], max = f[2, 2];
            for (int i = 2; i < nf - 2; i++)
            {
                for (int j = 2; j < nf - 2; j++)
                {
                    if (f[i, j] > max) max = f[i, j];
                    if (f[i, j] < min) min = f[i, j];
                }
            }
            float smax = max;
            max = 0.003f*a1*a2;
            /////////////////////////////////////////////////////////////////////////////////////////////////////
            Bitmap btm = new Bitmap(pictureBox1.Width,pictureBox1.Height);
            Graphics graph = Graphics.FromImage(btm);
            float n = 400;
            float nc = 1024;
            float k = nf-4;
            float hn = n/k;
            float hm = n*(a2/a1) / k;
            float hc = nc /(k-1);
            float hf = (max-min)/k;
            float c = 0;
            float cmax = 0;
            for (int j = 0; j < k; j++)
            {
                c = 0;
                r = 0; g = 0; b = 255;
                for (int i = 0; i < k; i++)
                {
                    c = hc * ((f[i + 2, j + 2] - min) / hf);
                    if (c > nc) c = 1024;
                    ConvColor(c);
                    graph.FillRectangle(new SolidBrush(Color.FromArgb(Convert.ToInt32(r), Convert.ToInt32(g), Convert.ToInt32(b))), i * hn, j*hm, hn, hm);
                    if (c > cmax) cmax = c;
                }
            }
            Console.WriteLine(Convert.ToString(cmax));
            Console.WriteLine(Convert.ToString(min));
            Console.WriteLine(Convert.ToString(max));
            pictureBox1.Image = btm;

            /////////////////////////////////////////////////////////////////////////////
            Bitmap btm2 = new Bitmap(pictureBox2.Width,pictureBox2.Height);
            Graphics graph2 = Graphics.FromImage(btm2);
            for (c = 0; c < nc; c+=2)
            {
                ConvColor(c);
                graph2.FillRectangle(new SolidBrush(Color.FromArgb(Convert.ToInt32(r), Convert.ToInt32(g), Convert.ToInt32(b))), c/2, 0, 1, 10);
            }
            pictureBox2.Image = btm2;
            label7.Text = Convert.ToString(min);
            label13.Text = Convert.ToString(max);
            label14.Text = "max = "+Convert.ToString(smax);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            q = Convert.ToSingle(textBox1.Text);
            a1 = Convert.ToSingle(textBox2.Text);
            a2 = Convert.ToSingle(textBox3.Text);
            a3 = Convert.ToSingle(textBox4.Text);
            E = Convert.ToSingle(textBox5.Text)* Convert.ToSingle(Math.Pow(10, 10));
            u = Convert.ToSingle(textBox6.Text);
            if (a1 < a2)
            {
                float kkk = a1;
                a1 = a2;
                a2 = kkk;
            }
            Draw();
        }
    }
}
