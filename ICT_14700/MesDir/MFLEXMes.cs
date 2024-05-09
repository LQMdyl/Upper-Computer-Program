using CommonHelper;
using MFLEX_Compass.TestDir;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading.Tasks;

namespace MFLEX_Compass.MesDir
{
    public class MFLEXMes
    {
        private readonly JsonParser jsonParser = new JsonParser();
        public string ApiAddress { get; set; }
        public string ApiPath { get; set; }
        public string Barcode { get; set; }
        public string OperatorID { get; set; }
        public string ToolNumber { get; set; }
        public string PreviousTestType { get; set; }
        public string TestType { get; set; }
        public string ProductName { get; set; }
        public string WorkArea { get; set; }
        public string Site { get; set; }
        public string slotName { get; set; }
        public string subslotName { get; set; }
        public string Program { get; set; }
        public string Lot { get; set; }
        public string IpAddress { get; set; }
        public string StationTime { get; set; }
        public DateTime TestTime { get; set; }
        public string TestResult { get; set; }
        public string ResourceName { get; set; }
        public string ErrorCode { get; set; }


        //    barcode：条码
        //    operator：操作员⼯号
        //    toolNumber：夹具编号
        //    testType：当前测试类型
        //    prevTestType：上⼀站测试类型
        //    productName：产品名称
        //    workArea：⻋间
        //    site：⼚区
        //    program：测试程序
        //    lot：流程单编号
        //    ipAddress：机台 IP 地址
        public object PreviousValidation(out string command, out string message)
        {
            command = message = "";

            WebResponse tmpWebResponse = null;
            StreamReader tmpStreamReader = null;

            try
            {
                #region Check input parameter

                if (string.IsNullOrEmpty(ApiAddress) || string.IsNullOrEmpty(ApiPath))
                {
                    message = "ET接口地址或是路径为空。";
                    return false;
                }

                if (string.IsNullOrEmpty(Barcode))
                {
                    message = "条码为空。";
                    return false;
                }

                if (string.IsNullOrEmpty(OperatorID))
                {
                    message = "操作员工号为空。";
                    return false;
                }

                if (string.IsNullOrEmpty(IpAddress))
                {
                    message = "机台IP地址为空。";
                    return false;
                }

                #endregion

                Barcode = Uri.EscapeDataString(Barcode);
                OperatorID = Uri.EscapeDataString(OperatorID);
                ToolNumber = Uri.EscapeDataString(ToolNumber ?? "");
                TestType = Uri.EscapeDataString(TestType ?? "");
                PreviousTestType = Uri.EscapeDataString(PreviousTestType ?? "");
                ProductName = Uri.EscapeDataString(ProductName ?? "");
                WorkArea = Uri.EscapeDataString(WorkArea ?? "");
                Site = Uri.EscapeDataString(Site ?? "");
                Program = Uri.EscapeDataString(Program ?? "");
                Lot = Uri.EscapeDataString(Lot ?? "");
                IpAddress = Uri.EscapeDataString(IpAddress ?? "");
                slotName = Uri.EscapeDataString("1");
                subslotName = Uri.EscapeDataString("1");

                if (ApiAddress.EndsWith("/")) ApiAddress = ApiAddress.Substring(0, ApiAddress.Length - 1);

                string tmpUrl = string.Format("{0}/{1}?barcode={2}&operator={3}&toolNumber={4}&testType={5}&prevTestType={6}&productName={7}&workArea={8}&site={9}&program={10}&lot={11}&ipAddress={12}&stationTime={13}&slotName={14}&subslotName={15}", ApiAddress, ApiPath, Barcode, OperatorID, ToolNumber, TestType, PreviousTestType, ProductName, WorkArea, Site, Program, Lot, IpAddress, StationTime, slotName, subslotName);
                command = tmpUrl;

                WebRequest tmpWebRequest = WebRequest.Create(tmpUrl);
                tmpWebRequest.Timeout = 5000;

                tmpWebResponse = tmpWebRequest.GetResponse();
                tmpStreamReader = new StreamReader(tmpWebResponse.GetResponseStream(), Encoding.UTF8);
                string tmpData = tmpStreamReader.ReadToEnd();

                message = tmpData ?? "";
                //object tmpObject = jsonParser.DeserializeStringToType<ETResult>(message);

                //return tmpObject != null && ((ETResult)tmpObject).isSuccess;

                return jsonParser.DeserializeStringToType<ETResult>(message);
            }
            catch (Exception ex)
            {
                message = string.Format("ET测试前校验错误 - {0}", ex.Message);
                return null;
            }
            finally
            {
                try
                {
                    if (tmpStreamReader != null) tmpStreamReader.Close();
                    if (tmpWebResponse != null) tmpWebResponse.Close();
                }
                catch
                {
                    // Ignored
                }
            }
        }
        public List<ETsample> GetShiftSamples(out string command, out string message)
        {
            command = message = "";

            WebResponse tmpWebResponse = null;
            StreamReader tmpStreamReader = null;

            try
            {
                #region Check input parameter

                if (string.IsNullOrEmpty(ApiAddress) || string.IsNullOrEmpty(ApiPath))
                {
                    message = "ET接口地址或是路径为空。";
                    return null;
                }

                if (string.IsNullOrEmpty(ToolNumber))
                {
                    message = "治具编号为空。";
                    return null;
                }

                #endregion
                ToolNumber = Uri.EscapeDataString(ToolNumber ?? "");
                if (ApiAddress.EndsWith("/")) ApiAddress = ApiAddress.Substring(0, ApiAddress.Length - 1);

                string tmpUrl = string.Format("{0}/{1}?resourcename={2}", ApiAddress, ApiPath, ToolNumber);
                command = tmpUrl;

                WebRequest tmpWebRequest = WebRequest.Create(tmpUrl);
                tmpWebRequest.Timeout = 5000;

                tmpWebResponse = tmpWebRequest.GetResponse();
                tmpStreamReader = new StreamReader(tmpWebResponse.GetResponseStream(), Encoding.UTF8);
                string tmpData = tmpStreamReader.ReadToEnd();

                message = tmpData ?? "";
                //object tmpObject = jsonParser.DeserializeStringToType<ETResult>(message);

                //return tmpObject != null && ((ETResult)tmpObject).isSuccess;

                return jsonParser.DeserializeStringToList<ETsample>(message);
            }
            catch (Exception ex)
            {
                message = string.Format("ET样品板当班有效记录获取错误 - {0}", ex.Message);
                return null;
            }
            finally
            {
                try
                {
                    if (tmpStreamReader != null) tmpStreamReader.Close();
                    if (tmpWebResponse != null) tmpWebResponse.Close();
                }
                catch
                {
                    // Ignored
                }
            }
        }

        public bool UploadTestResult(ETItem item, out string command, out string message)
        {
            //ETItem tmpItem = new ETItem()
            //{
            //    barcode = "1234567890",
            //    testType = "SOUND",
            //    testTime = DateTime.Now,
            //    testResult = "PASS",
            //    Operator = "73316",
            //    workArea = "HZ-A3",
            //    resourceName = "001",
            //    ipAddress = "192.168.3.3",
            //    toolNumber = "002",
            //    errorCode = null,
            //    productName = "693",
            //    program = "GTS001"
            //};

            message = "";
            command = "";

            if (item == null)
            {
                message = "上传数据项为空.\n";
                return false;
            }

            string tmpJsonData = Newtonsoft.Json.JsonConvert.SerializeObject(item);
            if (string.IsNullOrEmpty(tmpJsonData))
            {
                message = "生成Json数据错误.\n";
                return false;
            }

            tmpJsonData = tmpJsonData.Replace("Operator", "operator");
            command = tmpJsonData;

            return UploadData(tmpJsonData, out message);
        }

        private bool UploadData(string data, out string message)
        {
            message = "";

            HttpWebResponse tmpWebResponse = null;
            Stream tmpStream = null;
            StreamReader tmpStreamReader = null;

            try
            {
                string tmpUrl = string.Format("{0}/{1}", ApiAddress, ApiPath);
                byte[] tmpJsonBytes = Encoding.UTF8.GetBytes(data);
                int tmpLength = tmpJsonBytes.Length;

                var tmpWebRequest = (HttpWebRequest)WebRequest.Create(tmpUrl);
                tmpWebRequest.Method = "POST";
                tmpWebRequest.ContentType = "application/json;charset=UTF-8";
                tmpWebRequest.Headers.Add("Accept-Language", "zh-Hans,zh;q=0.9");
                tmpWebRequest.Timeout = 10000;
                tmpWebRequest.ContentLength = tmpLength;

                tmpStream = tmpWebRequest.GetRequestStream();
                tmpStream.Write(tmpJsonBytes, 0, tmpLength);

                tmpWebResponse = (HttpWebResponse)tmpWebRequest.GetResponse();
                tmpStreamReader = new StreamReader(tmpWebResponse.GetResponseStream(), Encoding.UTF8);
                string tmpData = tmpStreamReader.ReadToEnd();

                message = tmpData ?? "";
                object tmpObject = jsonParser.DeserializeStringToType<ETResult>(message);

                return tmpObject != null && ((ETResult)tmpObject).isSuccess;
            }
            catch (Exception ex)
            {
                message = string.Format("ET测试后上传测试结果错误 - {0}", ex.Message);
                return false;
            }
            finally
            {
                try
                {
                    if (tmpStream != null) tmpStream.Close();
                    if (tmpStreamReader != null) tmpStreamReader.Close();
                    if (tmpWebResponse != null) tmpWebResponse.Close();
                }
                catch
                {
                    // ignored
                }
            }
        }

        public bool CheckUserResult(ETuser userItem, out string command, out string message)
        {

            message = "";
            command = "";

            if (userItem == null)
            {
                message = "检验用户信息为空.\n";
                return false;
            }

            string tmpJsonData = Newtonsoft.Json.JsonConvert.SerializeObject(userItem);
            if (string.IsNullOrEmpty(tmpJsonData))
            {
                message = "生成Json数据错误.\n";
                return false;
            }
            command = tmpJsonData;
            return UploadUser(tmpJsonData, out message);
        }

        public bool UploadUser(string data, out string message)
        {
            message = "";

            HttpWebResponse tmpWebResponse = null;
            Stream tmpStream = null;
            StreamReader tmpStreamReader = null;

            try
            {
                string tmpUrl = string.Format("{0}/{1}", ApiAddress, ApiPath);
                byte[] tmpJsonBytes = Encoding.UTF8.GetBytes(data);
                int tmpLength = tmpJsonBytes.Length;

                var tmpWebRequest = (HttpWebRequest)WebRequest.Create(tmpUrl);
                tmpWebRequest.Method = "POST";
                tmpWebRequest.ContentType = "application/json;charset=UTF-8";
                tmpWebRequest.Headers.Add("Accept-Language", "zh-Hans,zh;q=0.9");
                tmpWebRequest.Timeout = 5000;
                tmpWebRequest.ContentLength = tmpLength;

                tmpStream = tmpWebRequest.GetRequestStream();
                tmpStream.Write(tmpJsonBytes, 0, tmpLength);

                tmpWebResponse = (HttpWebResponse)tmpWebRequest.GetResponse();
                tmpStreamReader = new StreamReader(tmpWebResponse.GetResponseStream(), Encoding.UTF8);
                string tmpData = tmpStreamReader.ReadToEnd();

                message = tmpData ?? "";
                object tmpObject = jsonParser.DeserializeStringToType<ETuserResult>(message);

                return tmpObject != null && ((ETuserResult)tmpObject).isSuccess;
            }
            catch (Exception ex)
            {
                message = string.Format("ET测试后上传测试结果错误 - {0}", ex.Message);
                return false;
            }
            finally
            {
                try
                {
                    if (tmpStream != null) tmpStream.Close();
                    if (tmpStreamReader != null) tmpStreamReader.Close();
                    if (tmpWebResponse != null) tmpWebResponse.Close();
                }
                catch
                {
                    // ignored
                }
            }
        }

    }

    public class ETItem
    {
        public string barcode { get; set; }
        public string testType { get; set; }
        public string testTime { get; set; }
        public string testResult { get; set; }
        public string Operator { get; set; }
        public string workArea { get; set; }
        public string resourceName { get; set; }
        public string ipAddress { get; set; }
        public string toolNumber { get; set; }
        public string errorCode { get; set; }
        // 2020-11-26 add
        public string errorValue { get; set; }
        public string productName { get; set; }
        public string program { get; set; }
        public string slotName { get; set; }
        public string subslotName { get; set; }
        public string socketInfo { get; set; }
        public string rosalineInfo { get; set; }
        public string testDetailId { get; set; }
        public string attribute1 { get; set; }
        public string attribute2 { get; set; }
        public string dartfishInfo { get; set; }
        public string extendInfo { get; set; }
        public List<ETDetail> testDetails { get; set; }
    }

    public class ETDetail
    {
        public string header { get; set; }
        public string upperLimit { get; set; }
        public string lowerLimit { get; set; }
        public string measureUnit { get; set; }
        public string value { get; set; }
    }

    public class ETResult
    {
        public bool isSuccess { get; set; }
        public string message { get; set; }
        public string currentTime { get; set; }
        public int extensionCode { get; set; } //判断测试次数
        public extensionMessages extensionMessages { get; set; }
        public string targetTestType { get; set; }
    }
    public class extensionMessages
    {
        public string BARCODE_FAMILY { get; set; }
        public string TESTED_COUNT { get; set; }
    }
    public class ETuser
    {
        public string userName { get; set; }
        public string password { get; set; }
        public int role { get; set; }
    }
    public class ETuserResult
    {
        public bool isSuccess { get; set; }
        public string message { get; set; }
    }
    public class ETsample
    {
        public string barcode { get; set; }
        public string testType { get; set; }
        public string testTime { get; set; }
        public string defectCode { get; set; }
        public bool isResultMatched { get; set; }
    }
}
