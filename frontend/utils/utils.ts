let connected = false;
export const isConnected = () => {
    return connected;
};

export const setConnected = (value: boolean) => {
    connected = value;
};

export async function getUniversityName(id: string) {
    try {
        const response = await $fetch(getAPI() + '/uni_prof/uni_info_by_id/' + id, {
            method: "GET",
            credentials: "include",
        });

        if (response.status === "success" && response.university) {
            return response.university.uni_name;
        } else {
            console.error("Error:", response);
            return "Unknown";
        }
    } catch (err) {
        console.error( err);
        return "Unknown";
    }
}

export async function getProfessorData(id: string) {
    try {
        const response = await $fetch(getAPI() + '/uni_prof/get_prof/' + id, {
            method: "GET",
            credentials: "include",
        });

        return response;
    } catch (err) {
        console.error( err);
        return {"name": "Unknown", "rating": null};
    }
}

export async function getReviews(course_id: string) {
    try {
        const response: Response = await $fetch(getAPI() + '/reviews/get_reviews_for_course/' + course_id, {
            method: "GET",
            credentials: "include",
        });
        return response;
    } catch (err) {
        console.error("Search failed:", err);
        await router.push("/");
        return [];
    }
}

export function getDepartments(course) {
    let departments_list = "";
    for(let department of course.value.departments || []) {
        departments_list = departments_list + ", " + department;
    }
    if(departments_list==="")
        return null;
    else
        return departments_list.slice(2);
}