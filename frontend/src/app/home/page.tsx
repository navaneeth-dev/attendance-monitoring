"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import PocketBase from "pocketbase";
import { Chart } from "react-google-charts";
import Image from "next/image";

const pb = new PocketBase(process.env.NEXT_PUBLIC_POCKETBASE_URL);

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toISOString().split("T")[0]; // Extract date part only
};

const HomePage = () => {
  const [attendance, setAttendance] = useState<
    { date: string; percentage: number }[]
  >([]);
  const [error, setError] = useState<string | null>(null);
  const [studentName, setStudentName] = useState<string | null>(null);
  const [chartData, setChartData] = useState<any[]>([
    ["Month", "Attendance Percentage"],
  ]); // Initial data with header

  const router = useRouter();

  useEffect(() => {
    const checkLogin = async () => {
      const registerNo = localStorage.getItem("registerNo");

      if (!registerNo) {
        router.push("/login"); // Redirect to login page if not logged in
        return;
      }

      try {
        // Fetch student info
        const student = await pb
          .collection("students")
          .getFirstListItem(`registerNo="${registerNo}"`);
        setStudentName(student.studName);

        // Fetch attendance records
        const records = await pb.collection("attendance").getFullList({
          filter: `registerNo="${registerNo}"`, // Filtering by registration number
        });

        // Prepare and sort the attendance data
        const attendanceData = records.map((record) => ({
          date: formatDate(record.date),
          percentage: record.percentage,
        }));

        // Sort data for the graph (ascending order by date)
        const sortedGraphData = [...attendanceData].sort(
          (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
        );

        // Set data for the chart
        const chartRows = sortedGraphData.map((record) => [
          record.date,
          record.percentage,
        ]);
        setChartData([["Month", "Attendance Percentage"], ...chartRows]);

        // Sort data for the table (descending order by date)
        const sortedTableData = [...attendanceData].sort(
          (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
        );

        // Set data for the table
        setAttendance(sortedTableData);
        setError(null);
      } catch (err) {
        setError("Failed to fetch data.");
        console.error("Error:", err);
      }
    };

    checkLogin();
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("registerNo");
    router.push("/login");
  };

  return (
    <>
      <div className="w-full ">
        <header className="max-w-screen-xl mx-auto bg-white shadow-md rounded-md">
          <nav className="flex justify-between items-center p-4">
            <div className="flex items-end ">
              <Image
                src="/ov.png"
                alt="OnlyVels AMS"
                width={1280}
                height={320}
                className="h-10 w-auto" // Adjust size as needed
              />
              <span className="font-medium text-xs">AMS</span>
            </div>
            <div className="flex items-center space-x-4">
              <div>
                {studentName && (
                  <span className="text-lg font-semibold text-gray-600">
                    Welcome, {studentName}
                  </span>
                )}
              </div>

              <button
                onClick={handleLogout}
                className="bg-[#00b0f0] text-white hover:bg-[#008ac9] focus:ring-4 focus:outline-none focus:ring-[##008ac9] font-medium rounded-lg text-sm px-4 py-2"
              >
                Logout
              </button>
            </div>
          </nav>
        </header>
      </div>
      <div className="max-w-screen-xl mx-auto mt-4">
        {error && <p className="text-red-500 text-center mt-4">{error}</p>}
        <div className="bg-white border border-gray-200 rounded-lg shadow-md p-4 mb-6">
          <Chart
            chartType="LineChart"
            width="100%"
            height="400px"
            data={chartData}
            options={{
              title: "Monthly Attendance Percentage",
              hAxis: { title: "Month" },
              vAxis: { title: "Percentage", minValue: 0, maxValue: 100 },
              legend: { position: "none" },
              curveType: "function",
              colors: ["#008dcf"],
              pointSize: 5, // Size of the points on the line
              pointShape: "circle", // Shape of the points (circle is default)
              lineWidth: 2, // Thickness of the line
            }}
          />
        </div>
        <div className="bg-white border border-gray-200 rounded-lg shadow-md p-4">
          <table className="min-w-full bg-white border border-gray-200 rounded-lg shadow-md">
            <thead>
              <tr className="bg-gray-100 border-b">
                <th className="py-3 px-4 text-left text-sm font-medium text-gray-900">
                  Date
                </th>
                <th className="py-3 px-4 text-left text-sm font-medium text-gray-900">
                  Percentage
                </th>
              </tr>
            </thead>
            <tbody>
              {attendance.length > 0 ? (
                attendance.map((record, index) => (
                  <tr key={index} className="border-b">
                    <td className="py-3 px-4 text-sm text-gray-900">
                      {record.date}
                    </td>
                    <td className="py-3 px-4 text-sm text-gray-900">
                      {record.percentage}%
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td
                    colSpan={2}
                    className="py-3 px-4 text-center text-gray-500"
                  >
                    No records found
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
};

export default HomePage;
