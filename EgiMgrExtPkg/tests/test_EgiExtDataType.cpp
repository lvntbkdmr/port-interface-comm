#include <gtest/gtest.h>
#include <EgiExtDataType.h>

class EgiExtDataTypeTest : public ::testing::Test {
protected:
    EgiExtDataType data;
};

TEST_F(EgiExtDataTypeTest, DefaultConstruction) {
    EgiExtDataType defaultData;
    // Struct should be default constructible
    SUCCEED();
}

TEST_F(EgiExtDataTypeTest, FieldAssignment) {
    data.exampleField = 42;
    EXPECT_EQ(data.exampleField, 42);
}

TEST_F(EgiExtDataTypeTest, FieldNegativeValue) {
    data.exampleField = -100;
    EXPECT_EQ(data.exampleField, -100);
}

TEST_F(EgiExtDataTypeTest, CopyConstruction) {
    data.exampleField = 123;
    EgiExtDataType copy = data;
    EXPECT_EQ(copy.exampleField, 123);
}

TEST_F(EgiExtDataTypeTest, Assignment) {
    data.exampleField = 456;
    EgiExtDataType other;
    other = data;
    EXPECT_EQ(other.exampleField, 456);
}
