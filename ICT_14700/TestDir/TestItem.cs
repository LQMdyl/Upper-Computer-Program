using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MFLEX_Compass.TestDir
{
    public class TestItem
    {
        public string Name { get; set; }
        public string High { get; set; }
        public string Low { get; set; }
        public string Unit { get; set; }
        public string Value { get; set; }
        public bool Result { get; set; }

        public TestItem()
        {
            Name = "";
            High = "";
            Low = "";
            Unit = "";
            Value = "";
            Result = false;
        }
    }
    public class Result
    {
        public List<TestItem> items { get; set; }
        public bool testResult { get; set; }
        public bool enable { get; set; }
        public int testTimes { get; set; }
        public string barcode { get; set; }
        public DateTime startTime { set; get; }
        public DateTime endTime { set; get; }
        public bool isSample { get; set;}

        public void initEntity()
        {
            this.items = new List<TestItem>();
            this.testResult = true;
            this.enable = true;
            this.testTimes = 1;
            this.startTime = DateTime.Now;
            this.endTime = DateTime.Now;
            this.barcode = "";
            this.isSample = false;
        }

        public Result()
        {

            this.items = new List<TestItem>();
            this.testResult = false;
            this.enable = true;
            this.testTimes = 1;
            this.startTime = DateTime.Now;
            this.endTime = DateTime.Now;
            this.barcode = "";
            this.isSample = false;
        }
    }
}
